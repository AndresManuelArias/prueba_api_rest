# api_rest

Ejercicio

## Developer Documentation

Comprehensive developer documentation is available in [`docs/dev/`](./docs/dev/) covering testing, configuration, deployment, and all project features.

### Quick Start for Developers

```bash
# Install development environment
make install

# Start services with Docker
docker compose up -d

# Start aplication
docker compose up --build

# Run tests
make tests

# Auto-fix formatting
make chores
```

See the [developer documentation](./docs/dev/README.md) for complete guides and reference.

### run aplication local
```bash

uvicorn api_rest.www:app --reload

```

### Migration
create archive
```bash

docker compose exec www alembic revision --autogenerate -m "create users table"
```
create table
```bash

docker compose exec www alembic upgrade head
```
