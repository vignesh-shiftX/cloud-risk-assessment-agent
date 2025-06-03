import pytest
import os
import yaml
import json
from datetime import datetime
from src.scan.kubernetes import scan_kubernetes, k8s_resource_misconfigure
from src.scan.filesystem import scan_filesystem, process_code_scan
from src.scan.image import scan_image
from src.scan.aws import scan_aws, gen_aws_db_content
import pandas as pd

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

@pytest.fixture
def sample_k8s_manifest():
    return {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": "test-pod"},
        "spec": {
            "containers": [{
                "name": "test",
                "image": "nginx:latest",
                "securityContext": {
                    "privileged": True,
                    "runAsNonRoot": False
                },
                "resources": {}
            }]
        }
    }

@pytest.fixture
def sample_aws_scan_result():
    return {
        "results": [
            {
                "type": "aws",
                "id": "AWS001",
                "resource": "s3-bucket",
                "service": "s3",
                "status": "FAIL",
                "message": "Bucket is publicly accessible",
                "severity": "HIGH"
            },
            {
                "type": "aws",
                "id": "AWS002",
                "resource": "security-group",
                "service": "ec2",
                "status": "FAIL",
                "message": "Security group allows all inbound traffic",
                "severity": "CRITICAL"
            }
        ]
    }

class TestKubernetesScan:
    """Test suite for Kubernetes scanning functionality"""

    @pytest.mark.asyncio
    async def test_kubernetes_scan_basic(self, tmp_path):
        """Test basic Kubernetes scanning functionality"""
        config_path = tmp_path / "config"
        with open(config_path, "w") as f:
            f.write("apiVersion: v1\nkind: Config\n")
        
        result = await scan_kubernetes(str(config_path))
        assert isinstance(result, dict)
        assert "results" in result

    @pytest.mark.asyncio
    async def test_kubernetes_scan_with_invalid_config(self, tmp_path):
        """Test Kubernetes scanning with invalid config"""
        config_path = tmp_path / "invalid_config"
        with open(config_path, "w") as f:
            f.write("invalid yaml content")
        
        with pytest.raises(Exception):
            await scan_kubernetes(str(config_path))

    def test_k8s_resource_misconfigure_comprehensive(self, sample_k8s_manifest):
        """Test comprehensive Kubernetes misconfiguration detection"""
        issues = k8s_resource_misconfigure(sample_k8s_manifest)
        assert len(issues) > 0
        
        # Check for specific security issues
        found_issues = {issue["id"]: issue for issue in issues}
        
        # Check privileged container
        assert any(
            issue["severity"] == "HIGH" and "privileged" in issue["message"].lower() 
            for issue in issues
        )
        
        # Check latest tag usage
        assert any(
            issue["severity"] in ["MEDIUM", "HIGH"] and "latest" in issue["message"].lower() 
            for issue in issues
        )
        
        # Check resource limits
        assert any(
            "resource" in issue["message"].lower() 
            for issue in issues
        )

    @pytest.mark.parametrize("manifest_modification,expected_issues", [
        ({"spec": {"hostNetwork": True}}, "host network"),
        ({"spec": {"containers": [{"name": "test", "securityContext": {"privileged": True}}]}}, "privileged"),
        ({"spec": {"containers": [{"name": "test", "image": "nginx:latest"}]}}, "latest"),
        ({"spec": {"containers": [{"name": "test", "resources": {}}]}}, "resource limits"),
    ])
    def test_k8s_specific_misconfigurations(self, sample_k8s_manifest, manifest_modification, expected_issues):
        """Test specific Kubernetes misconfigurations"""
        manifest = sample_k8s_manifest.copy()
        # Deep update the manifest
        for key, value in manifest_modification.items():
            if isinstance(value, dict):
                manifest.setdefault(key, {}).update(value)
            else:
                manifest[key] = value
        
        issues = k8s_resource_misconfigure(manifest)
        assert any(expected_issues in issue["message"].lower() for issue in issues)

class TestCodeScan:
    """Test suite for code scanning functionality"""

    @pytest.mark.asyncio
    async def test_code_scan_comprehensive(self, tmp_path):
        """Test comprehensive code repository scanning"""
        code_dir = tmp_path / "code"
        code_dir.mkdir()
        
        # Create multiple test files with different security issues
        files = {
            "test1.py": 'password = "hardcoded_password"\napi_key = "secret_key"',
            "test2.py": 'os.system(user_input)  # Command injection',
            "config.json": '{"password": "123456", "debug": true}',
            "Dockerfile": 'FROM ubuntu:latest\nRUN apt-get update\nEXPOSE 22',
        }
        
        for filename, content in files.items():
            with open(code_dir / filename, "w") as f:
                f.write(content)
        
        result = await scan_filesystem(str(code_dir))
        assert isinstance(result, dict)
        assert "results" in result
        assert len(result["results"]) > 0
        
        # Verify different types of issues are detected
        issues = result["results"]
        assert any("password" in str(issue).lower() for issue in issues)
        assert any("command injection" in str(issue).lower() for issue in issues)
        assert any("dockerfile" in str(issue).lower() for issue in issues)

    @pytest.mark.asyncio
    async def test_process_code_scan_comprehensive(self):
        """Test comprehensive code scan result processing"""
        sample_result = {
            "results": [
                {
                    "type": "sast",
                    "ruleId": "TEST001",
                    "location": {"path": "test.py", "lines": {"begin": 1}},
                    "message": "Hardcoded password",
                    "severity": "HIGH"
                },
                {
                    "type": "secret",
                    "ruleId": "TEST002",
                    "location": {"path": "config.json", "lines": {"begin": 5}},
                    "message": "API key exposed",
                    "severity": "CRITICAL"
                },
                {
                    "type": "dependency",
                    "ruleId": "TEST003",
                    "location": {"path": "requirements.txt", "lines": {"begin": 10}},
                    "message": "Vulnerable dependency",
                    "severity": "MEDIUM"
                }
            ]
        }
        
        df = await process_code_scan(sample_result, type="CODE")
        assert not df.empty
        assert all(col in df.columns for col in ["severity", "type", "message", "file"])
        assert len(df) == len(sample_result["results"])
        assert "HIGH" in df["severity"].values
        assert "CRITICAL" in df["severity"].values

class TestContainerScan:
    """Test suite for container scanning functionality"""

    @pytest.mark.asyncio
    async def test_container_scan_comprehensive(self, tmp_path):
        """Test comprehensive container image scanning"""
        image_path = tmp_path / "test.tar"
        
        # Create a mock container image tar with layers
        os.makedirs(tmp_path / "layers")
        with open(tmp_path / "layers" / "layer1.tar", "wb") as f:
            f.write(b"layer1 content")
        
        # Create manifest.json
        manifest = [{
            "Config": "config.json",
            "Layers": ["layers/layer1.tar"]
        }]
        with open(tmp_path / "manifest.json", "w") as f:
            json.dump(manifest, f)
        
        # Create config.json
        config = {
            "config": {
                "ExposedPorts": {"22/tcp": {}},
                "Env": ["PASSWORD=test123"]
            }
        }
        with open(tmp_path / "config.json", "w") as f:
            json.dump(config, f)
        
        result = await scan_image(str(image_path))
        assert isinstance(result, dict)
        assert "results" in result

class TestAWSScan:
    """Test suite for AWS scanning functionality"""

    @pytest.mark.asyncio
    async def test_aws_scan_comprehensive(self, mocker):
        """Test comprehensive AWS resource scanning"""
        # Mock AWS API calls
        mocker.patch('boto3.client')
        result = await scan_aws("us-west-2")
        assert isinstance(result, dict)
        assert "results" in result

    @pytest.mark.asyncio
    async def test_aws_db_content_comprehensive(self, sample_aws_scan_result):
        """Test comprehensive AWS scan result processing"""
        columns = ["type", "id", "resource_name", "service_name", "severity", "message"]
        df = await gen_aws_db_content(sample_aws_scan_result, columns)
        
        assert not df.empty
        assert all(col in df.columns for col in columns)
        assert len(df) == len(sample_aws_scan_result["results"])
        
        # Verify data content
        assert "HIGH" in df["severity"].values
        assert "CRITICAL" in df["severity"].values
        assert "s3" in df["service_name"].values
        assert "ec2" in df["service_name"].values
        
        # Test severity distribution
        severity_counts = df["severity"].value_counts()
        assert severity_counts["HIGH"] >= 1
        assert severity_counts["CRITICAL"] >= 1

    @pytest.mark.asyncio
    async def test_aws_scan_with_filters(self, mocker):
        """Test AWS scanning with various filters"""
        # Mock AWS API calls
        mock_client = mocker.patch('boto3.client')
        
        # Test different regions
        await scan_aws("us-east-1")
        mock_client.assert_called_with(mocker.ANY, region_name="us-east-1")
        
        # Test with service filters
        await scan_aws("us-west-2", services=["s3", "ec2"])
        # Add assertions for service filtering

    @pytest.mark.asyncio
    async def test_aws_scan_error_handling(self, mocker):
        """Test AWS scanning error handling"""
        # Mock AWS API errors
        mocker.patch('boto3.client', side_effect=Exception("AWS API Error"))
        
        with pytest.raises(Exception) as exc_info:
            await scan_aws("us-west-2")
        assert "AWS API Error" in str(exc_info.value) 