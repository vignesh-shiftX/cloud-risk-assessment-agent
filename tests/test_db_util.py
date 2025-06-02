import pytest
import os
import sqlite3
import asyncio
from src.db.db_util import init_db, init_sample, batch_upsert_records
from src.db.config import DEFAULT_DB_PATH

@pytest.fixture
def temp_db_path(tmp_path):
    """Create a temporary database path"""
    return str(tmp_path / "test.db")

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