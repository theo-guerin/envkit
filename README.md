# EnvKit

*A lightweight package for parsing environment variables.*

## Installation

```bash
pip install envkit
```

## Usage

```python
from envkit import Fields

# Required string with minimum length
api_key = Fields.str("API_KEY", min_length=32)

# Optional integer with default and range
port = Fields.int("PORT", default=8080, min_value=1, max_value=65535)

# Boolean with default
debug = Fields.bool("DEBUG", default=False)

# Enum parsing
log_level = Fields.enum("LOG_LEVEL", enum=LogLevel, default=LogLevel.INFO)
```

## Contributing

Contributions are welcome!
Whether you want to report an issue, suggest an improvement, or submit a pull
request, your help is appreciated.

If you’re new to open source, feel free to participate as well — the project is
open to contributors of all experience levels.

- Open an issue for bugs, ideas, or questions
- Submit a pull request with changes or enhancements
- Documentation and test improvements are also valuable

Everyone is welcome to contribute.
