import pytest
from src.scan.cvss_score import safe_cvss_score
from src.util.cvss import calculate_cvss_score, parse_cvss_vector, get_severity_level

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

class TestCVSSScore:
    """Test suite for CVSS scoring functionality"""

    @pytest.mark.parametrize("vector,expected_score", [
        ("AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", 9.8),  # Critical severity
        ("AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H", 8.8),  # High severity
        ("AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:L", 5.6),  # Medium severity
        ("AV:L/AC:H/PR:H/UI:R/S:U/C:L/I:L/A:L", 3.0),  # Low severity
        ("AV:P/AC:H/PR:H/UI:R/S:U/C:L/I:N/A:N", 1.6),  # Low severity
    ])
    def test_calculate_cvss_score(self, vector, expected_score):
        """Test CVSS score calculation with various vectors"""
        score = calculate_cvss_score(vector)
        assert abs(score - expected_score) < 0.1  # Allow small floating point differences

    @pytest.mark.parametrize("vector,expected_components", [
        (
            "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
            {
                "AV": "N",  # Attack Vector: Network
                "AC": "L",  # Attack Complexity: Low
                "PR": "N",  # Privileges Required: None
                "UI": "N",  # User Interaction: None
                "S": "U",   # Scope: Unchanged
                "C": "H",   # Confidentiality: High
                "I": "H",   # Integrity: High
                "A": "H"    # Availability: High
            }
        ),
        (
            "AV:L/AC:H/PR:H/UI:R/S:C/C:L/I:L/A:N",
            {
                "AV": "L",  # Attack Vector: Local
                "AC": "H",  # Attack Complexity: High
                "PR": "H",  # Privileges Required: High
                "UI": "R",  # User Interaction: Required
                "S": "C",   # Scope: Changed
                "C": "L",   # Confidentiality: Low
                "I": "L",   # Integrity: Low
                "A": "N"    # Availability: None
            }
        )
    ])
    def test_parse_cvss_vector(self, vector, expected_components):
        """Test CVSS vector parsing with various vectors"""
        components = parse_cvss_vector(vector)
        assert components == expected_components

    @pytest.mark.parametrize("score,expected_severity", [
        (9.8, "CRITICAL"),
        (8.9, "HIGH"),
        (7.0, "HIGH"),
        (6.9, "MEDIUM"),
        (4.0, "MEDIUM"),
        (3.9, "LOW"),
        (0.1, "LOW"),
        (10.0, "CRITICAL"),
        (0.0, "NONE"),
    ])
    def test_get_severity_level(self, score, expected_severity):
        """Test severity level determination for various scores"""
        severity = get_severity_level(score)
        assert severity == expected_severity

    def test_invalid_cvss_vector(self):
        """Test handling of invalid CVSS vectors"""
        invalid_vectors = [
            "",  # Empty string
            "Invalid",  # Invalid format
            "AV:X/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",  # Invalid Attack Vector
            "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H",  # Missing component
            "AV:N/AC:L/PR:N/UI:N/S:U/C:Z/I:H/A:H",  # Invalid value
        ]
        for vector in invalid_vectors:
            with pytest.raises(ValueError):
                calculate_cvss_score(vector)

    def test_invalid_cvss_scores(self):
        """Test handling of invalid CVSS scores"""
        invalid_scores = [
            -1,     # Negative score
            11,     # Score > 10
            "abc",  # Non-numeric
            None,   # None value
        ]
        for score in invalid_scores:
            with pytest.raises(ValueError):
                get_severity_level(score)

    @pytest.mark.parametrize("vector,component,expected", [
        ("AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", "AV", "N"),
        ("AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", "AC", "L"),
        ("AV:L/AC:H/PR:H/UI:R/S:C/C:L/I:L/A:N", "S", "C"),
    ])
    def test_vector_component_extraction(self, vector, component, expected):
        """Test extraction of specific components from CVSS vectors"""
        components = parse_cvss_vector(vector)
        assert components[component] == expected

    def test_cvss_score_ranges(self):
        """Test CVSS score ranges and boundaries"""
        # Test score ranges
        assert get_severity_level(9.0) == "CRITICAL"
        assert get_severity_level(8.9) == "HIGH"
        assert get_severity_level(7.0) == "HIGH"
        assert get_severity_level(6.9) == "MEDIUM"
        assert get_severity_level(4.0) == "MEDIUM"
        assert get_severity_level(3.9) == "LOW"
        assert get_severity_level(0.1) == "LOW"
        
        # Test boundary conditions
        assert get_severity_level(10.0) == "CRITICAL"  # Maximum score
        assert get_severity_level(0.0) == "NONE"      # Minimum score 