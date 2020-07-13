"""Reads dotenv file(s) and updates os.environ

# Environment Variables

* `DOTENV_PATH` - identifies the path to the .env file(s) to load.  For multiple files, use a comma separated list.
                  DOTENV_PATH will also be interpreted just like the .dotenv files, so $HOME and $PWD is a legal path.

* `DOTENV_DEBUG` - if set to a true value ("1", "y", "yes", "true", "t", "on"), then the identification of which
                   file(s) were loaded and the final values of the dotenv file entries will be shown

"""
import os
from pathlib import Path
from typing import Dict, List, Optional

from .extract import get_env_debug, get_env_paths
from .interpolate import interpolate_paths
from .parse import parse_dotenv
from .read import read_dotenv


def load(debug: Optional[bool] = None, paths: Optional[List[str]] = None, update_env: bool = True,) -> Dict[str, str]:
    """Reads and parses dotenv and then updates os.environ with new values

    This method will also return the resulting environment loaded.

    # Arguments

    * `debug` - Adds stdout messages for what files were processed and final environment variable values
    * `paths` - Optionally override the environment variable with a set of paths to dotenv files
    * `update_env` - if set to true, then os.environ will be updated [default is True]

    """
    debug = get_env_debug(debug=debug)
    paths = get_env_paths(paths=paths)
    environ = {key: value for key, value in os.environ.items()}
    found = {}
    for path in interpolate_paths(paths=paths):
        if Path(path).exists() and Path(path).is_file():
            data = read_dotenv(path, debug=debug)
            parsed = parse_dotenv(data, debug=debug, env=environ)
            found.update(parsed)
            environ.update(found)
    if update_env:
        os.environ.update(found)
    return found
