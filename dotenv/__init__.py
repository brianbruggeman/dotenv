"""Reads dotenv file(s) and updates os.environ

# Environment Variables

* `DOTENV_PATH` - identifies the path to the .env file(s) to load.  For multiple files, use a comma separated list.
                  DOTENV_PATH will also be interpreted just like the .dotenv files, so $HOME and $PWD is a legal path.

* `DOTENV_DEBUG` - if set to a true value ("1", "y", "yes", "true", "t", "on"), then the identification of which
                   file(s) were loaded and the final values of the dotenv file entries will be shown

"""
__version__ = "0.1.0"

from .load import load
