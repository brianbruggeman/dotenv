"""Extracts environment variables from environment variable values"""
import os
from typing import List, Optional

from .constants import DEFAULT_DOTENV_DEBUG, DEFAULT_DOTENV_PATH, DOTENV_DEBUG_VARNAME, DOTENV_PATH_VARNAME


def get_env_debug(debug: Optional[bool]) -> bool:
    """Get debug from environment
    """
    env_value = os.environ.get(DOTENV_DEBUG_VARNAME, DEFAULT_DOTENV_DEBUG)
    if debug is None:
        if env_value.lower() in ["1", "on", "t", "true", "yes", "y"]:
            debug = True
        elif env_value.lower() in ["0", "off", "f", "false", "no", "n"]:
            debug = False
    if debug is None:
        debug = False
    return debug


def get_env_paths(paths: Optional[List[str]] = None) -> List[str]:
    """Extracts paths from environment variable
    """
    if paths is None:
        path_env_value = os.environ.get(DOTENV_PATH_VARNAME, DEFAULT_DOTENV_PATH)
        env_paths = path_env_value.split(",")
    else:
        env_paths = [p for p in paths]
    return env_paths


def extract_variables(value: str) -> List[str]:
    """Extracts environment variables from value

    Reads through string and extracts potential environment variables by searching for the character "$" followed by
    a standard variable name (e.g. VAR, var, Var, Var01, var_02, ...)
    """
    names = set()
    valid_chars = list(range(ord("a"), ord("z"))) + list(range(ord("A"), ord("Z"))) + list(range(ord("1"), ord("0"))) + [ord("_")]
    collecting = False
    word = ""
    for index, char in enumerate(value):
        if char == "$":
            if collecting is False:
                collecting = True
                continue
            elif word:
                names.add(word)
                word = ""
                continue
        if collecting:
            if ord(char) in valid_chars:
                word += char
            else:
                collecting = False
                if word:
                    names.add(word)
                    word = ""
    if word and collecting is True:
        names.add(word)
    return sorted(names)
