import pytest
import os
import json
from src.scan.scan_result import ScanResult, ReportFormatException

@pytest.fixture
def sample_scan_result():
    return ScanResult()

@pytest.fixture
def sample_kubernetes_report():
    return {
        "results": [
            {
                "type": "kubernetes",
                "id": "KSV001",
                "title": "Privileged container",
                "description": "Container is running in privileged mode",
                "severity": "HIGH",
                "message": "Container 'nginx' in Pod 'web' is running in privileged mode",
                "resource_name": "web-pod",
                "service_name": "default"
            }
        ]
    }

def test_scan_result_initialization(sample_scan_result):
    """Test that ScanResult is initialized correctly"""
    assert sample_scan_result is not None
    assert hasattr(sample_scan_result, 'get_scan_result')

def test_get_scan_result_nonexistent(sample_scan_result):
    """Test getting scan result for non-existent scan type"""
    result = sample_scan_result.get_scan_result("nonexistent")
    assert result is None

def test_get_scan_result_kubernetes(sample_scan_result, sample_kubernetes_report, tmp_path):
    """Test getting Kubernetes scan results"""
    # Create a temporary results directory
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    
    # Write sample report
    report_path = results_dir / "kubernetes.json"
    with open(report_path, "w") as f:
        json.dump(sample_kubernetes_report, f)
    
    # Set the results directory path
    sample_scan_result.results_dir = str(results_dir)
    
    # Get the scan result
    result = sample_scan_result.get_scan_result("kubernetes")
    assert result is not None
    assert result["results"][0]["type"] == "kubernetes"
    assert result["results"][0]["id"] == "KSV001"

def test_get_scan_result_invalid_json(sample_scan_result, tmp_path):
    """Test handling of invalid JSON in results file"""
    # Create a temporary results directory
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    
    # Write invalid JSON
    report_path = results_dir / "kubernetes.json"
    with open(report_path, "w") as f:
        f.write("invalid json")
    
    # Set the results directory path
    sample_scan_result.results_dir = str(results_dir)
    
    # Attempt to get the scan result
    with pytest.raises(ReportFormatException):
        sample_scan_result.get_scan_result("kubernetes") 