import pytest
import os
import json
import stat
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

def test_get_scan_result_multiple_types(sample_scan_result, tmp_path):
    """Test getting scan results for multiple scan types"""
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    # Write two reports
    kubernetes_report = {"results": [{"type": "kubernetes", "id": "KSV001"}]}
    aws_report = {"results": [{"type": "aws", "id": "AWS001"}]}
    with open(results_dir / "kubernetes.json", "w") as f:
        json.dump(kubernetes_report, f)
    with open(results_dir / "aws.json", "w") as f:
        json.dump(aws_report, f)
    sample_scan_result.results_dir = str(results_dir)
    k8s_result = sample_scan_result.get_scan_result("kubernetes")
    aws_result = sample_scan_result.get_scan_result("aws")
    assert k8s_result["results"][0]["type"] == "kubernetes"
    assert aws_result["results"][0]["type"] == "aws"

def test_get_scan_result_empty_file(sample_scan_result, tmp_path):
    """Test handling of empty results file"""
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    report_path = results_dir / "kubernetes.json"
    with open(report_path, "w") as f:
        f.write("")
    sample_scan_result.results_dir = str(results_dir)
    with pytest.raises(ReportFormatException):
        sample_scan_result.get_scan_result("kubernetes")

def test_get_scan_result_permission_error(sample_scan_result, tmp_path):
    """Test handling of permission error when reading results file"""
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    report_path = results_dir / "kubernetes.json"
    with open(report_path, "w") as f:
        f.write("{}")
    # Remove read permissions
    os.chmod(report_path, 0)
    sample_scan_result.results_dir = str(results_dir)
    try:
        with pytest.raises(Exception):
            sample_scan_result.get_scan_result("kubernetes")
    finally:
        # Restore permissions so tmp_path can be cleaned up
        os.chmod(report_path, stat.S_IWUSR | stat.S_IRUSR)

def test_get_scan_result_directory_traversal(sample_scan_result, tmp_path):
    """Test directory traversal attempt in scan type name"""
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    sample_scan_result.results_dir = str(results_dir)
    # Try to traverse directories
    with pytest.raises(Exception):
        sample_scan_result.get_scan_result("../etc/passwd")

def test_get_scan_result_partial_json(sample_scan_result, tmp_path):
    """Test handling of partial/corrupted JSON file"""
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    report_path = results_dir / "kubernetes.json"
    with open(report_path, "w") as f:
        f.write("{\"results\": [")  # Incomplete JSON
    sample_scan_result.results_dir = str(results_dir)
    with pytest.raises(ReportFormatException):
        sample_scan_result.get_scan_result("kubernetes") 