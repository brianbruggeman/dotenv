# dotenv
![Python package](https://github.com/brianbruggeman/dotenv/workflows/Python%20package/badge.svg)

Yet another dotenv package

# Motivation

I wanted a sane interface for dotenv and I didn't want to wait for an upstream package maintainer to update their
code.

# Usage

## Basic usage

```python
import dotenv

dotenv.load()
```

## Environment Variables

* `DOTENV_PATH` - a comma delimited sequence of paths to load [default: `PWD`/.env]
* `DOTENV_DEBUG` - this will display the paths, values read and values interpolated if set to true [default: False]

## dotenv DSL

* `comments` - comments can be delimited with a `#` and will be ignored
* `ENV_NAME=ENV_VALUE` - The expectation is that every variable setting have an equal sign to notate key and value
* `-ENV_NAME` - it is also possible to remove environment variables

