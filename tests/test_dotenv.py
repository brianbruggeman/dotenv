"""Tests simple use cases for dotenv"""
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

import pytest

environ = {key: value for key, value in os.environ.items()}


@dataclass
class TC:
    """Test case for extract method"""

    # files represents filename => filecontents mapping.  Everything will be created under a tmp folder
    files: Dict[str, str] = field(default_factory=dict)
    dotenv_path: str = ""
    update_env: bool = True
    expected: Dict[str, str] = field(default_factory=dict)
    original: Dict[str, str] = field(
        repr=False, init=False, default_factory=lambda: {key: value for key, value in os.environ.items()},
    )


test_cases = [
    TC(),
    TC(dotenv_path=".env1"),
    TC(dotenv_path=".env2,test2.env"),
    TC(files={".env3": "REPO=$HOME/repos/dotenv"}, dotenv_path=".env3,test3.env", expected={"REPO": "{HOME}/repos/dotenv"},),
    TC(
        files={
            ".env4": """
        REPO=$HOME/repos/dotenv
        MOD_PATH=$REPO/mods
        """,
            "test4.env": "MOD_PATH=$HOME/mods",
        },
        dotenv_path=".env4,test4.env",
        expected={"REPO": "{HOME}/repos/dotenv", "MOD_PATH": "{HOME}/mods"},
    ),
    TC(
        files={".env5": "REPO=$HOME/repos/dotenv", "test5.env": "MOD_PATH=$REPO/mods"},
        dotenv_path=".env5,test5.env",
        expected={"REPO": "{HOME}/repos/dotenv", "MOD_PATH": "{HOME}/repos/dotenv/mods",},
    ),
]


# Best case here would be to store the current value and then restore in the teardown, but this should work
def setup_environment(test_case: TC, tmpdir):
    from dotenv.constants import DOTENV_PATH_VARNAME

    folders = []
    for found in reversed(sorted(Path(tmpdir).glob("**/*"))):
        if found.is_file():
            found.unlink()
            print(f"Removed: {found}")
        elif found.is_dir():
            folders.append(found)

    for folder in reversed(sorted(folders)):
        folder.unlink()
        print(f"Removed: {folder}")

    paths = []
    for path in test_case.dotenv_path.split(","):
        dotenv_path = Path(tmpdir) / path
        if dotenv_path:
            paths.append(str(dotenv_path))
    if paths:
        os.environ[DOTENV_PATH_VARNAME] = ",".join(paths)
    for filename, contents in test_case.files.items():
        filepath = Path(tmpdir) / filename
        filepath.write_text(contents, "utf-8")
        assert filepath.read_text("utf-8") == contents
        print(f"Wrote to: {filepath}")
    if paths:
        for path in os.environ.get(DOTENV_PATH_VARNAME, "").split(","):
            print(f"DOTENV_PATH: {path}")


def teardown_environment(test_case: TC):
    from dotenv.constants import DOTENV_PATH_VARNAME

    os.environ.pop(DOTENV_PATH_VARNAME)
    for key in test_case.expected:
        os.environ.pop(key)
    os.environ.update(test_case.original)


@pytest.mark.parametrize("test_case", test_cases, ids=list(map(str, test_cases)))
def test_load(test_case, tmpdir):
    from dotenv import load

    setup_environment(test_case, tmpdir)
    result = load(update_env=test_case.update_env)
    for key, value in test_case.expected.items():
        expected_value = value.format(**os.environ)
        assert key in result
        assert result.get(key) == expected_value
        if test_case.update_env:
            assert key in os.environ
            assert os.environ.get(key) == expected_value
    teardown_environment(test_case)
