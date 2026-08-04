# EnvKit

[![PyPI - Version](https://img.shields.io/pypi/v/envkit)](https://pypi.org/project/envkit/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/envkit)](https://pypi.org/project/envkit/)

A lightweight, strongly‑typed environment variable parser focused on explicit configuration and predictable behavior, inspired by [environs](https://github.com/sloria/environs).

## Installation

```bash
pip install envkit
```

## Usage

```python
from envkit import Env

# Required string with minimum length
api_key = Env.str("API_KEY", min_length=32)

# Optional integer with default and range
port = Env.int("PORT", required=False, default=8080, min_value=1, max_value=65535)

# Boolean with default
debug = Env.bool("DEBUG", required=False, default=False)

# Enum parsing
log_level = Env.enum("LOG_LEVEL", enum=LogLevel, required=False, default=LogLevel.INFO)
```
