"""Reads dotenv file and returns raw string if file exists"""
from pathlib import Path
from typing import Optional


def read_dotenv(path: Path, debug: bool = False) -> Optional[str]:
    """Extracts raw string from a file

    Reads a dotenv file and returns the raw data
    """
    data = None if not path.exists() else path.read_text("utf-8")
    if debug:
        message = f"Read: `{path}`" if data is not None else f"Could not find: `{path}`"
        print(message)
    return data
