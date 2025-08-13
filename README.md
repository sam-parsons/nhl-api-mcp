# NHL API MCP Server (Scaffold)

A Model Context Protocol (MCP) server scaffold for NHL data. This repository mirrors the setup of `mlb-api-mcp` (packaging, tooling, Docker, Smithery, entrypoint), but intentionally omits NHL implementation for now.

## Installation (uv)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone <your-repo-url> nhl-api-mcp
cd nhl-api-mcp
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Run

- Stdio transport (for MCP clients):
```bash
uv run python main.py
```

- HTTP transport:
```bash
uv run python main.py --http
# or choose a port
uv run python main.py --http --port 8000
```

## Docker

```bash
docker build -t nhl-api-mcp .
docker run -p 8000:8000 nhl-api-mcp
# with local timezone
docker run -e TZ=America/New_York -p 8000:8000 nhl-api-mcp
```

## Development

- Python 3.10+ (Docker uses Python 3.12)
- FastMCP, FastAPI, uvicorn
- uv for env/run, Hatchling for build
- Ruff for linting

Pre-commit (optional):
```bash
pip install pre-commit
pre-commit install
```

## Testing

Scaffold includes pytest + coverage wiring. Threshold is temporarily 0 until tests/implementation are added.

```bash
uv run pytest
```

## Endpoints (HTTP mode)

- `/` → redirects to `/docs`
- `/docs` → basic documentation
- `/health`
- `/info`
- `/tools` (will be empty until tools are added)

Implementation of NHL tools will be added later.
