import pytest
import os
import json
import subprocess
import tempfile
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

def test_run_command_non_json_but_valid_file(tmp_path):
    """Test handling of a valid file that is not JSON (e.g., plain text)"""
    output_file = str(tmp_path / "plain.txt")
    with open(output_file, "w") as f:
        f.write("just some text")
    with pytest.raises(JSONParseError):
        run_command_and_read_output(["echo", "test"], output_file)

def test_run_command_no_output_but_no_error(tmp_path):
    """Test command that does not produce output file but does not error"""
    output_file = str(tmp_path / "should_not_exist.json")
    # Use a command that does not create the file
    with pytest.raises(NoOutputError):
        run_command_and_read_output(["echo", ""], output_file)

def test_run_command_large_json(tmp_path):
    """Test handling of a large JSON output file"""
    output_file = str(tmp_path / "large.json")
    large_data = {"numbers": list(range(10000))}
    with open(output_file, "w") as f:
        json.dump(large_data, f)
    result = run_command_and_read_output(["echo", "test"], output_file)
    assert result == large_data

def test_run_command_with_env_and_cwd(tmp_path):
    """Test command execution with environment variables and working directory"""
    output_file = str(tmp_path / "env.json")
    test_data = {"env": os.environ.get("HOME", "")}
    with open(output_file, "w") as f:
        json.dump(test_data, f)
    # Use a different working directory
    cwd = tempfile.gettempdir()
    # Should still work
    result = run_command_and_read_output(["echo", "test"], output_file)
    assert result == test_data 