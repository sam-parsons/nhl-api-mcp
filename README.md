# NHL API MCP Server (Scaffold)

[![CI](https://github.com/sam-parsons/nhl-api-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/sam-parsons/nhl-api-mcp/actions/workflows/ci.yml)
[![Docker Hub](https://img.shields.io/docker/pulls/samparsons269/nhl-api-mcp.svg)](https://hub.docker.com/r/samparsons269/nhl-api-mcp)
[![Docker Image Size](https://img.shields.io/docker/image-size/samparsons269/nhl-api-mcp/latest)](https://hub.docker.com/r/samparsons269/nhl-api-mcp)


## 📦 Package Builds

This project automatically builds Python packages on every push to main. Build artifacts are available in the [GitHub Actions](https://github.com/sam-parsons/nhl-api-mcp/actions) workflow.

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

## MCP Configuration

To use this MCP server with MCP clients (like Cursor), you'll need to create an `mcp.json` configuration file. Here's how to set it up for the Docker container:

Create or edit an `mcp.json` file in your MCP client (ex: Cursor)'s configuration directory:

```json
{
  "mcpServers": {
    "nhl-api": {
      "url": "http://localhost:8000/mcp/"
    }
  }
}
```

After creating the configuration file, restart your MCP client to connect to the NHL API server.

## Development

- Python 3.10+ (Docker uses Python 3.12)
- FastMCP, uvicorn
- uv for env/run, Hatchling for build

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
- `/tools` → lists all available NHL API tools

## Available NHL API Tools

This MCP server provides comprehensive access to NHL data through the following categories:

### Teams & Rosters
- Get all NHL teams with conference/division info
- Get team rosters by season
- Get team prospects
- Get franchise information
- Get team ID mappings

### Standings & Seasons
- Get current league standings
- Get standings for specific dates or seasons
- Get season metadata and manifest

### Schedules
- Get daily/weekly game schedules
- Get team-specific schedules (monthly, weekly, season)
- Get playoff schedules and brackets

### Statistics (NEW!)
- **Game Types by Team**: Get all game types played by a team throughout history
- **Player Career Stats**: Comprehensive player statistics and biographical information
- **Player Game Logs**: Game-by-game statistics for specific seasons
- **Team Summary Stats**: Team performance statistics across seasons
- **Skater Stats**: Detailed skater statistics with filtering options
- **Goalie Stats**: Goalie performance metrics with multiple report types

For detailed documentation on the Stats API tools, see [STATS_API_README.md](STATS_API_README.md).

## Example Usage

```python
from nhl_api import get_nhl_teams, get_nhl_player_career_stats

# Get all NHL teams
teams = get_nhl_teams()

# Get Connor McDavid's career stats
mcdavid_stats = get_nhl_player_career_stats("8478402")
```

See `example_stats_usage.py` for comprehensive examples of the Stats API functions.

Implementation of NHL tools will be added later.
