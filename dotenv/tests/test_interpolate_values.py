"""Tests simple use cases for dotenv"""
import os
from dataclasses import dataclass, field
from typing import Dict

import pytest


@dataclass
class TC:
    """Test case for extract method"""

    value: str = ""
    environ: Dict[str, str] = field(default_factory=dict)
    expected: str = ""


environ = {key: value for key, value in os.environ.items()}

test_cases = [
    TC("", {}, ""),
    TC("$HOME", {}, "$HOME"),
    TC("$HOME", environ, "{HOME}"),
    TC("$PWD", environ, "{PWD}"),
]


@pytest.mark.parametrize("test_case", test_cases, ids=list(map(str, test_cases)))
def test_interpolate_values(test_case):
    from ..interpolate import interpolate_values

    found = interpolate_values(test_case.value, test_case.environ)
    assert found == test_case.expected.format(**environ)
