import pytest
import os
import yaml
from src.scan.kubernetes import scan_kubernetes, k8s_resource_misconfigure
from src.scan.filesystem import scan_filesystem, process_code_scan
from src.scan.image import scan_image
from src.scan.aws import scan_aws, gen_aws_db_content

@pytest.fixture
def sample_config():
    return {
        "kubernetes": {
            "config_path": "/tmp/tmcybertron/.kube/config"
        },
        "code": {
            "folder": "/tmp/tmcybertron/repo/test"
        },
        "container": {
            "image_path": "/tmp/tmcybertron/image_file/test.tar"
        },
        "aws": {
            "region": "us-west-2"
        }
    }

@pytest.mark.asyncio
async def test_kubernetes_scan(tmp_path):
    """Test Kubernetes scanning functionality"""
    config_path = tmp_path / "config"
    with open(config_path, "w") as f:
        f.write("apiVersion: v1\nkind: Config\n")
    
    result = await scan_kubernetes(str(config_path))
    assert isinstance(result, dict)
    assert "results" in result

@pytest.mark.asyncio
async def test_code_scan(tmp_path):
    """Test code repository scanning"""
    # Create a test file with potential security issue
    code_dir = tmp_path / "code"
    code_dir.mkdir()
    test_file = code_dir / "test.py"
    with open(test_file, "w") as f:
        f.write("password = 'hardcoded_password'\n")
    
    result = await scan_filesystem(str(code_dir))
    assert isinstance(result, dict)
    assert "results" in result

@pytest.mark.asyncio
async def test_container_scan(tmp_path):
    """Test container image scanning"""
    # Create a dummy container tar
    image_path = tmp_path / "test.tar"
    with open(image_path, "wb") as f:
        f.write(b"dummy container data")
    
    result = await scan_image(str(image_path))
    assert isinstance(result, dict)
    assert "results" in result

@pytest.mark.asyncio
async def test_aws_scan():
    """Test AWS resource scanning"""
    result = await scan_aws("us-west-2")
    assert isinstance(result, dict)
    assert "results" in result

@pytest.mark.asyncio
async def test_process_code_scan():
    """Test code scan result processing"""
    sample_result = {
        "results": [
            {
                "type": "sast",
                "ruleId": "TEST001",
                "location": {
                    "path": "test.py",
                    "lines": {"begin": 1}
                },
                "message": "Test vulnerability",
                "severity": "HIGH"
            }
        ]
    }
    
    df = await process_code_scan(sample_result, type="CODE")
    assert not df.empty
    assert "severity" in df.columns
    assert "type" in df.columns

@pytest.mark.asyncio
async def test_aws_db_content():
    """Test AWS scan result processing"""
    sample_result = {
        "results": [
            {
                "type": "aws",
                "id": "AWS001",
                "resource": "s3-bucket",
                "service": "s3",
                "status": "FAIL",
                "message": "Bucket is publicly accessible"
            }
        ]
    }
    
    df = await gen_aws_db_content(sample_result, ["type", "id", "resource_name", "service_name", "severity", "message"])
    assert not df.empty
    assert "service_name" in df.columns
    assert "severity" in df.columns

def test_k8s_resource_misconfigure():
    """Test Kubernetes misconfiguration detection"""
    test_manifest = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": "test-pod"},
        "spec": {
            "containers": [{
                "name": "test",
                "image": "nginx",
                "securityContext": {
                    "privileged": True
                }
            }]
        }
    }
    
    issues = k8s_resource_misconfigure(test_manifest)
    assert len(issues) > 0
    assert any(issue["severity"] == "HIGH" for issue in issues) 