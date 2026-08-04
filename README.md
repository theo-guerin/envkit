# EnvKit

[![CI](https://github.com/theo-guerin/envkit/actions/workflows/release.yml/badge.svg)](https://github.com/theo-guerin/envkit/actions/workflows/release.yml)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/theo-guerin/envkit/actions/workflows/release.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/envkit)](https://pypi.org/project/envkit/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/envkit)](https://pypi.org/project/envkit/)
[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/envkit)](https://pypi.org/project/envkit/)
[![PyPI - Types](https://img.shields.io/pypi/types/envkit)](https://pypi.org/project/envkit/)
[![PyPI - License](https://img.shields.io/pypi/l/envkit)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://docs.astral.sh/uv/)

A lightweight, strongly‑typed environment variable parser focused on explicit configuration and predictable behavior, inspired by [environs](https://github.com/sloria/environs).

- Zero runtime dependencies, requires Python 3.12+
- Precise return types via overloads: no `| None` when a variable is required or has a default
- Runtime validation: length and range bounds, enum membership, literal choices
- Ships `py.typed`, checked with mypy (strict), basedpyright, ty, and pyrefly

## Installation

```bash
pip install envkit
```

## Usage

```python
from enum import Enum

from envkit import Env


class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3


# Required string with minimum length (returns str)
api_key = Env.str("API_KEY", min_length=32)

# Optional integer with default and range (returns int)
port = Env.int("PORT", required=False, default=8080, min_value=1, max_value=65535)

# Boolean with default (returns bool)
debug = Env.bool("DEBUG", required=False, default=False)

# Enum parsing by member name (returns LogLevel)
log_level = Env.enum("LOG_LEVEL", LogLevel, required=False, default=LogLevel.INFO)

# Optional without default (returns str | None)
hostname = Env.str("HOSTNAME", required=False)
```

## Behavior

- A missing **required** variable raises `KeyError`.
- A value that fails to parse or validate raises `ValueError`.
- An unset variable with `required=False` returns `default` (`None` if no default is given). An empty string counts as set.
- `int`, `float`, `bool`, and `enum` values are stripped of surrounding whitespace before parsing.
