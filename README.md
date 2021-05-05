# Leginorma

[![Build Status](https://github.com/envinorma/leginorma/workflows/Build%20Main/badge.svg)](https://github.com/envinorma/leginorma/actions)
[![Documentation](https://github.com/envinorma/leginorma/workflows/Documentation/badge.svg)](https://envinorma.github.io/leginorma/)
[![Code Coverage](https://codecov.io/gh/envinorma/leginorma/branch/main/graph/badge.svg)](https://codecov.io/gh/envinorma/leginorma)

Python wrapper for Legifrance API

---

## Features

-   Store values and retain the prior value in memory
-   ... some other functionality

## Quick Start

```python
from leginorma import LegifranceText, LegifranceClient

client = LegifranceClient('client_id', 'client_secret')
text = LegifranceText.from_dict(client.consult_law_decree('JORFTEXT000034429274'))
```

## Installation

**Stable Release:** `pip install leginorma`<br>
**Development Head:** `pip install git+https://github.com/envinorma/leginorma.git`

## Documentation

For full package documentation please visit [envinorma.github.io/leginorma](https://envinorma.github.io/leginorma).

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for information related to developing the code.

**MIT license**
