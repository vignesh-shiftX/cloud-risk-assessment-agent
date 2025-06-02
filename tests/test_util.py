import pytest
import os
import json
import subprocess
from src.scan.util import run_command_and_read_output, JSONParseError, NoOutputError

def test_run_command_success(tmp_path):
    """Test successful command execution and JSON parsing"""
    # Create a temporary output file with valid JSON
    output_file = str(tmp_path / "output.json")
    test_data = {"key": "value"}
    with open(output_file, "w") as f:
        json.dump(test_data, f)
    
    # Run a simple command that succeeds
    result = run_command_and_read_output(["echo", "test"], output_file)
    assert result == test_data

def test_run_command_no_output(tmp_path):
    """Test handling of missing output file"""
    output_file = str(tmp_path / "nonexistent.json")
    
    with pytest.raises(NoOutputError):
        run_command_and_read_output(["echo", "test"], output_file)

def test_run_command_invalid_json(tmp_path):
    """Test handling of invalid JSON in output file"""
    output_file = str(tmp_path / "invalid.json")
    
    # Create file with invalid JSON
    with open(output_file, "w") as f:
        f.write("invalid json")
    
    with pytest.raises(JSONParseError):
        run_command_and_read_output(["echo", "test"], output_file)

def test_run_command_execution_error():
    """Test handling of command execution failure"""
    with pytest.raises(subprocess.CalledProcessError):
        run_command_and_read_output(["nonexistent_command"], "output.json") 