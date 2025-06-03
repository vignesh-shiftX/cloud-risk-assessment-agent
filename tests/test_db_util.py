import pytest
import os
import sqlite3
import asyncio
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.db.db_util import (
    init_db,
    init_sample,
    batch_upsert_records,
    create_connection,
    insert_scan_results,
    get_scan_results,
    filter_results,
    update_scan_result,
    delete_scan_result,
    get_scan_history,
    get_severity_distribution,
    get_resource_type_distribution
)
from src.db.config import DEFAULT_DB_PATH

@pytest.fixture
def temp_db_path(tmp_path):
    """Create a temporary database path"""
    return str(tmp_path / "test.db")

@pytest.fixture
def sample_scan_results():
    """Fixture for sample scan results data"""
    return pd.DataFrame({
        'id': range(1, 6),
        'scan_id': ['scan1'] * 5,
        'timestamp': [datetime.now() - timedelta(days=i) for i in range(5)],
        'type': ['aws', 'kubernetes', 'code', 'container', 'aws'],
        'resource_name': ['s3-bucket', 'pod', 'app.py', 'nginx:latest', 'ec2-instance'],
        'service_name': ['s3', 'k8s', 'code', 'docker', 'ec2'],
        'severity': ['HIGH', 'CRITICAL', 'MEDIUM', 'LOW', 'HIGH'],
        'message': [f'Test issue {i}' for i in range(1, 6)],
        'status': ['OPEN'] * 5,
        'remediation': ['Fix issue'] * 5
    })

@pytest.fixture
def db_connection():
    """Fixture for database connection"""
    conn = create_connection(':memory:')  # Use in-memory SQLite for testing
    return conn

@pytest.mark.asyncio
async def test_init_db(temp_db_path):
    """Test database initialization"""
    success = await init_db(temp_db_path)
    assert success is True
    assert os.path.exists(temp_db_path)

    # Verify table structure
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    
    # Check if results table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='results'")
    assert cursor.fetchone() is not None
    
    conn.close()

@pytest.mark.asyncio
async def test_init_sample(temp_db_path):
    """Test sample data initialization"""
    success = await init_sample(temp_db_path)
    assert success is True
    
    # Verify sample data was inserted
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM results")
    count = cursor.fetchone()[0]
    assert count > 0
    conn.close()

@pytest.mark.asyncio
async def test_batch_upsert_records(temp_db_path):
    """Test batch upserting of records"""
    # Initialize the database first
    await init_db(temp_db_path)
    
    # Test data
    test_records = [
        {
            "type": "test",
            "id": "TEST001",
            "resource_name": "test-resource",
            "service_name": "test-service",
            "title": "Test Issue",
            "description": "Test Description",
            "severity": "LOW",
            "message": "Test Message"
        }
    ]
    
    # Perform the upsert
    success = await batch_upsert_records(test_records, db_path=temp_db_path)
    assert success is True
    
    # Verify the records were inserted
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM results WHERE id=?", ("TEST001",))
    record = cursor.fetchone()
    assert record is not None
    assert record[1] == "TEST001"  # id field
    assert record[2] == "test-resource"  # resource_name field
    conn.close()

@pytest.mark.asyncio
async def test_batch_upsert_duplicate_records(temp_db_path):
    """Test upserting duplicate records"""
    # Initialize the database
    await init_db(temp_db_path)
    
    # Test data with duplicate ID
    test_records = [
        {
            "type": "test",
            "id": "TEST001",
            "resource_name": "test-resource-1",
            "service_name": "test-service",
            "title": "Test Issue 1",
            "description": "Test Description 1",
            "severity": "LOW",
            "message": "Test Message 1"
        },
        {
            "type": "test",
            "id": "TEST001",  # Same ID
            "resource_name": "test-resource-2",
            "service_name": "test-service",
            "title": "Test Issue 2",
            "description": "Test Description 2",
            "severity": "MEDIUM",
            "message": "Test Message 2"
        }
    ]
    
    # Perform the upsert
    success = await batch_upsert_records(test_records, db_path=temp_db_path)
    assert success is True
    
    # Verify only the latest record exists
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM results WHERE id=?", ("TEST001",))
    count = cursor.fetchone()[0]
    assert count == 1  # Should only be one record
    
    cursor.execute("SELECT resource_name, severity FROM results WHERE id=?", ("TEST001",))
    record = cursor.fetchone()
    assert record[0] == "test-resource-2"  # Should have the latest values
    assert record[1] == "MEDIUM"
    conn.close()

class TestDatabaseOperations:
    """Test suite for database operations"""

    def test_create_connection(self):
        """Test database connection creation"""
        conn = create_connection(':memory:')
        assert conn is not None
        cursor = conn.cursor()
        # Verify we can execute a simple query
        cursor.execute('SELECT 1')
        assert cursor.fetchone()[0] == 1

    def test_insert_scan_results(self, db_connection, sample_scan_results):
        """Test inserting scan results into database"""
        # Insert sample data
        success = insert_scan_results(db_connection, sample_scan_results)
        assert success
        
        # Verify insertion
        cursor = db_connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM scan_results')
        count = cursor.fetchone()[0]
        assert count == len(sample_scan_results)

    @pytest.mark.parametrize("filter_params", [
        {"severity": ["HIGH"]},
        {"type": ["aws"]},
        {"service_name": ["s3"]},
        {"status": ["OPEN"]},
        {"severity": ["HIGH", "CRITICAL"], "type": ["aws", "kubernetes"]},
        {"since": datetime.now() - timedelta(days=7)},
        {"until": datetime.now()},
    ])
    def test_filter_results(self, db_connection, sample_scan_results, filter_params):
        """Test filtering scan results with various parameters"""
        # Insert test data
        insert_scan_results(db_connection, sample_scan_results)
        
        # Apply filters
        filtered_results = filter_results(db_connection, **filter_params)
        assert isinstance(filtered_results, pd.DataFrame)
        assert not filtered_results.empty
        
        # Verify filters are applied correctly
        if "severity" in filter_params:
            assert all(sev in filter_params["severity"] for sev in filtered_results["severity"])
        if "type" in filter_params:
            assert all(t in filter_params["type"] for t in filtered_results["type"])

    def test_update_scan_result(self, db_connection, sample_scan_results):
        """Test updating scan result status and remediation"""
        # Insert test data
        insert_scan_results(db_connection, sample_scan_results)
        
        # Update first result
        result_id = sample_scan_results.iloc[0]["id"]
        updates = {
            "status": "FIXED",
            "remediation": "Issue has been resolved",
            "resolution_time": datetime.now()
        }
        success = update_scan_result(db_connection, result_id, updates)
        assert success
        
        # Verify update
        cursor = db_connection.cursor()
        cursor.execute('SELECT status, remediation FROM scan_results WHERE id = ?', (result_id,))
        updated = cursor.fetchone()
        assert updated[0] == "FIXED"
        assert updated[1] == "Issue has been resolved"

    def test_delete_scan_result(self, db_connection, sample_scan_results):
        """Test deleting scan results"""
        # Insert test data
        insert_scan_results(db_connection, sample_scan_results)
        
        # Delete first result
        result_id = sample_scan_results.iloc[0]["id"]
        success = delete_scan_result(db_connection, result_id)
        assert success
        
        # Verify deletion
        cursor = db_connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM scan_results WHERE id = ?', (result_id,))
        count = cursor.fetchone()[0]
        assert count == 0

    def test_get_scan_history(self, db_connection, sample_scan_results):
        """Test retrieving scan history"""
        # Insert test data
        insert_scan_results(db_connection, sample_scan_results)
        
        # Get history
        history = get_scan_history(db_connection)
        assert isinstance(history, pd.DataFrame)
        assert not history.empty
        assert "scan_id" in history.columns
        assert "timestamp" in history.columns
        assert len(history) > 0

    def test_get_severity_distribution(self, db_connection, sample_scan_results):
        """Test getting severity distribution"""
        # Insert test data
        insert_scan_results(db_connection, sample_scan_results)
        
        # Get distribution
        distribution = get_severity_distribution(db_connection)
        assert isinstance(distribution, pd.DataFrame)
        assert not distribution.empty
        assert "severity" in distribution.columns
        assert "count" in distribution.columns
        
        # Verify counts
        severity_counts = sample_scan_results["severity"].value_counts()
        for severity, count in severity_counts.items():
            assert distribution[distribution["severity"] == severity]["count"].iloc[0] == count

    def test_get_resource_type_distribution(self, db_connection, sample_scan_results):
        """Test getting resource type distribution"""
        # Insert test data
        insert_scan_results(db_connection, sample_scan_results)
        
        # Get distribution
        distribution = get_resource_type_distribution(db_connection)
        assert isinstance(distribution, pd.DataFrame)
        assert not distribution.empty
        assert "type" in distribution.columns
        assert "count" in distribution.columns
        
        # Verify counts
        type_counts = sample_scan_results["type"].value_counts()
        for type_, count in type_counts.items():
            assert distribution[distribution["type"] == type_]["count"].iloc[0] == count

    def test_error_handling(self, db_connection):
        """Test error handling in database operations"""
        # Test invalid data insertion
        invalid_df = pd.DataFrame({
            'invalid_column': ['test']
        })
        with pytest.raises(Exception):
            insert_scan_results(db_connection, invalid_df)
        
        # Test invalid update
        with pytest.raises(Exception):
            update_scan_result(db_connection, 999, {"invalid_field": "value"})
        
        # Test invalid deletion
        with pytest.raises(Exception):
            delete_scan_result(db_connection, 999)

    def test_concurrent_operations(self, db_connection, sample_scan_results):
        """Test concurrent database operations"""
        # Insert initial data
        insert_scan_results(db_connection, sample_scan_results)
        
        # Simulate concurrent operations
        for _ in range(5):
            # Update operation
            update_scan_result(db_connection, 1, {"status": "IN_PROGRESS"})
            # Read operation
            results = get_scan_results(db_connection)
            assert not results.empty
            # Filter operation
            filtered = filter_results(db_connection, severity=["HIGH"])
            assert not filtered.empty

    def test_large_dataset_handling(self, db_connection):
        """Test handling of large datasets"""
        # Create large dataset
        large_df = pd.DataFrame({
            'scan_id': ['scan_large'] * 1000,
            'timestamp': [datetime.now()] * 1000,
            'type': np.random.choice(['aws', 'kubernetes', 'code', 'container'], 1000),
            'resource_name': [f'resource_{i}' for i in range(1000)],
            'service_name': [f'service_{i}' for i in range(1000)],
            'severity': np.random.choice(['HIGH', 'MEDIUM', 'LOW', 'CRITICAL'], 1000),
            'message': [f'Test message {i}' for i in range(1000)],
            'status': ['OPEN'] * 1000,
            'remediation': ['To be fixed'] * 1000
        })
        
        # Test insertion of large dataset
        success = insert_scan_results(db_connection, large_df)
        assert success
        
        # Test retrieval and filtering of large dataset
        results = get_scan_results(db_connection)
        assert len(results) == 1000
        
        filtered = filter_results(db_connection, severity=['HIGH'])
        assert len(filtered) > 0 