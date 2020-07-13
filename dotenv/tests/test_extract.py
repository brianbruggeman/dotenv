"""Tests simple use cases for dotenv"""
from dataclasses import dataclass, field
from typing import List

import pytest


@dataclass
class TC:
    """Test case for extract method"""

    value: str = ""
    expected: List[str] = field(default_factory=list)


test_cases = [
    TC("", []),
    TC("abc", []),
    TC("abc 123 abc_123", []),
    TC("ABC 123 abc_123", []),
    TC("$ABC 123 abc_123", ["ABC"]),
    TC("$ABC $ABC", ["ABC"]),
    TC("$DEF $ABC", ["ABC", "DEF"]),
    TC("$HOME$ABC", ["ABC", "HOME"]),
    TC("s3://$BUCKET/$KEY_PREFIX$KEY_SUFFIX", ["BUCKET", "KEY_PREFIX", "KEY_SUFFIX"]),
]


@pytest.mark.parametrize("test_case", test_cases, ids=list(map(str, test_cases)))
def test_extract(test_case):
    from ..extract import extract_variables

    found = extract_variables(test_case.value)
    assert found == test_case.expected
