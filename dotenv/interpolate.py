import os
from pathlib import Path
from typing import Dict, List, Optional

from .extract import extract_variables


def interpolate_values(value: str, env: Optional[Dict[str, str]] = None) -> str:
    environ = {key: value for key, value in env.items()} if env is not None else {}
    varnames = extract_variables(value)
    for varname in varnames:
        if varname in environ:
            val = environ[varname]
            value = value.replace(f"${varname}", val)
    return value


def interpolate_paths(paths: List[str]):
    environ = {key: value for key, value in os.environ.items()}
    good_paths: List[Path] = []
    for path in paths:
        path = interpolate_values(value=path, env=environ)
        if path:
            good_paths.append(Path(path))
    return good_paths
