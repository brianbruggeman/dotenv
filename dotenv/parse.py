"""Parses dotenv file for standard dotenv lines
"""
import os
from typing import Dict, Optional

from .interpolate import interpolate_values


def remove_comments(line: str) -> str:
    """Removes comments from line"""
    if "#" in line:
        line = line.split("#", 1)[0]
    return line


def fix_key(key: str) -> str:
    """fixes key if needed"""
    key = key.strip()
    if key.lower().startswith("export "):
        key = key[7:]
    return key


def parse_dotenv(data, debug: bool = False, env: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """Extracts key value pairs from data

    # Rules

    * `removal` - remove a key by prefacing with a '-'
    * `comment` - comments begin with a #
    * `export` - if a line starts with 'export', the export is ignored

    """
    if env is None:
        env = {key: value for key, value in os.environ.items()}
    updates: Dict[str, str] = {}
    if data is not None:
        for line in data.splitlines():
            # remove comments
            line = remove_comments(line)
            if not line.strip():
                continue
            # ignore non-setter lines
            if "=" not in line:
                key = fix_key(line.strip())
                value = ""
                if key.startswith("-"):
                    # remove keys
                    key = key.lstrip("-")
                    if env and key in env:
                        env.pop(key)
                    if updates and key in updates:
                        updates.pop(key)
                    continue
            else:
                key, value = line.split("=", 1)
                key = fix_key(key)
            updates[key] = value
    for key, value in updates.items():
        value = interpolate_values(value, updates)
        value = interpolate_values(value, env)
        updates[key] = value
    if debug:
        for key, value in sorted(updates.items()):
            print(f"{key}={value}")
    updated: Dict[str, str] = {key: value for key, value in updates.items()}
    return updated
