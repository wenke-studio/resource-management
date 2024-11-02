# Resource Management

## Requirements

- Python 3.12 
    - uv 0.4.13

## Quick Start

```bash
uv sync
uvicorn app.main:app --reload
```

## Roadmap

1. Import `alembic` to manage migrations
2. dockerize this application
3. implement unit tests
4. setup custom logging
5. setup CI/CD using github actions
    - gitlab runner is optional