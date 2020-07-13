"""Tests simple use cases for dotenv"""
import os
from dataclasses import dataclass, field
from typing import Dict

import pytest


@dataclass
class TC:
    """Test case for extract method"""

    lines: str = ""
    expected: Dict[str, str] = field(default_factory=dict)

    environ: Dict[str, str] = field(repr=False, default_factory=lambda: {key: value for key, value in os.environ.items()})


test_cases = [
    TC(),
    TC("-DOTENV_PATH"),
    TC("    DOTENV_PATH=$HOME/.env", {"DOTENV_PATH": "{HOME}/.env"}),
    TC("export DOTENV_PATH=$HOME/.env", {"DOTENV_PATH": "{HOME}/.env"}),
    TC("#export DOTENV_PATH=$HOME/.env"),
    TC("      # export DOTENV_PATH=$HOME/.env"),
    TC("DOTENV_PATH=$HOME/.env", {"DOTENV_PATH": "{HOME}/.env"}),
    # Removal 2.0
    TC(
        lines="""
            DOTENV_PATH=$HOME/.env
            -DOTENV_PATH
        """
    ),
    # Tests internal dotenv references
    TC(
        lines="""
            REPO=$HOME/repos/dotenv
            DOTENV_PATH=$REPO/.env
            """,
        expected={"REPO": "{HOME}/repos/dotenv", "DOTENV_PATH": "{HOME}/repos/dotenv/.env",},
    ),
    # Tests internal dotenv references
    TC(
        lines="""
            -HOME
            REPO=$HOME/repos/dotenv
            DOTENV_PATH=$REPO/.env
            """,
        expected={"REPO": "$HOME/repos/dotenv", "DOTENV_PATH": "$HOME/repos/dotenv/.env",},
    ),
]


@pytest.mark.parametrize("test_case", test_cases, ids=list(map(str, test_cases)))
def test_parse_dotenv(test_case):
    from ..parse import parse_dotenv

    found = parse_dotenv(test_case.lines, env=test_case.environ)
    expected = {key: value.format(**test_case.environ) for key, value in test_case.expected.items()}
    assert found == expected
