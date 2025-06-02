import pytest
from src.scan.cvss_score import safe_cvss_score

def test_valid_cvss_score():
    """Test calculation of CVSS score with valid input"""
    # Test a valid CVSS v3 string
    cvss_string = "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
    score = safe_cvss_score(cvss_string)
    assert score == 9.8  # This is the expected score for this vector

def test_none_cvss_score():
    """Test handling of None input"""
    score = safe_cvss_score(None)
    assert score is None

def test_invalid_cvss_score():
    """Test handling of invalid CVSS string"""
    invalid_cvss = "INVALID:STRING"
    score = safe_cvss_score(invalid_cvss)
    assert score is None

def test_empty_cvss_score():
    """Test handling of empty string"""
    score = safe_cvss_score("")
    assert score is None

def test_malformed_cvss_score():
    """Test handling of malformed CVSS string"""
    malformed_cvss = "CVSS:3.1/AV:N/AC:L"  # Incomplete CVSS string
    score = safe_cvss_score(malformed_cvss)
    assert score is None 