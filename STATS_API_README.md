# NHL Stats API Tools

This document describes the new NHL Stats API tools that have been added to the NHL API wrapper. These tools provide access to comprehensive hockey statistics including player stats, team stats, and game logs.

## Overview

The Stats API tools are built on top of the `nhlpy` library's Stats class and provide a simplified interface for accessing NHL statistics data. All functions include proper error handling and return consistent response formats.

## Available Tools

### 1. Game Types Per Season by Team

**Function:** `get_nhl_gametypes_per_season_by_team(team_abbr)`

**Description:** Gets all game types played by a team throughout their history.

**Parameters:**
- `team_abbr` (str): The 3 letter abbreviation of the team (e.g., BUF, TOR, BOS)

**Returns:** Dictionary containing game types for each season the team has existed.

**Example:**
```python
from nhl_api import get_nhl_gametypes_per_season_by_team

result = get_nhl_gametypes_per_season_by_team("TOR")
if "gametypes" in result:
    for season_data in result["gametypes"]:
        print(f"Season {season_data['season']}: {season_data['gameTypes']}")
```

**Response Format:**
```json
{
  "gametypes": [
    {"season": 20242025, "gameTypes": [2]},
    {"season": 20232024, "gameTypes": [2, 3]},
    {"season": 20222023, "gameTypes": [2, 3]}
  ]
}
```

**Game Type Codes:**
- 1: Preseason
- 2: Regular Season  
- 3: Playoffs

### 2. Player Career Stats

**Function:** `get_nhl_player_career_stats(player_id)`

**Description:** Gets a player's career statistics and biographical information.

**Parameters:**
- `player_id` (str): The unique identifier for the NHL player

**Returns:** Dictionary containing comprehensive player data including stats and personal information.

**Example:**
```python
from nhl_api import get_nhl_player_career_stats

result = get_nhl_player_career_stats("8478402")  # Connor McDavid
if "player_stats" in result:
    stats = result["player_stats"]
    print(f"{stats['firstName']['default']} {stats['lastName']['default']}")
    print(f"Position: {stats['position']}")
    print(f"Team: {stats['currentTeamAbbrev']}")
```

### 3. Player Game Log

**Function:** `get_nhl_player_game_log(player_id, season_id, game_type)`

**Description:** Gets a player's game-by-game statistics for a specific season and game type.

**Parameters:**
- `player_id` (str): The unique identifier for the NHL player
- `season_id` (str): Season in YYYYYYYY format (e.g., "20242025")
- `game_type` (int): Type of games (1=Preseason, 2=Regular, 3=Playoffs)

**Returns:** List of dictionaries containing game-by-game statistics.

**Example:**
```python
from nhl_api import get_nhl_player_game_log

result = get_nhl_player_game_log("8478402", "20242025", 2)  # Regular season
if "game_log" in result:
    for game in result["game_log"][:5]:  # First 5 games
        print(f"{game['gameDate']}: {game['goals']}G {game['assists']}A")
```

### 4. Team Summary Stats

**Function:** `get_nhl_team_summary_stats(start_season, end_season, game_type_id, is_game, is_aggregate, start, limit)`

**Description:** Retrieves team summary statistics across one or more seasons.

**Parameters:**
- `start_season` (str): Beginning season in YYYYYYYY format
- `end_season` (str): Ending season in YYYYYYYY format
- `game_type_id` (int, optional): Game type (default: 2 for regular season)
- `is_game` (bool, optional): Default False
- `is_aggregate` (bool, optional): Whether to aggregate statistics (default: False)
- `start` (int, optional): Starting index for pagination (default: 0)
- `limit` (int, optional): Maximum results to return (default: 50)

**Returns:** List of dictionaries containing team summary statistics.

**Example:**
```python
from nhl_api import get_nhl_team_summary_stats

result = get_nhl_team_summary_stats("20202021", "20212022", 2)
if "team_summary" in result:
    for team in result["team_summary"]:
        print(f"{team['teamFullName']}: {team['points']} points")
```

### 5. Skater Stats Summary

**Function:** `get_nhl_skater_stats_summary(start_season, end_season, franchise_id, game_type_id, aggregate, start, limit)`

**Description:** Gets simplified skater statistics summary for specified seasons and franchises.

**Parameters:**
- `start_season` (str): Beginning season in YYYYYYYY format
- `end_season` (str): Ending season in YYYYYYYY format
- `franchise_id` (str, optional): Franchise identifier for filtering
- `game_type_id` (int, optional): Game type (default: 2 for regular season)
- `aggregate` (bool, optional): Combine multiple seasons per player (default: False)
- `start` (int, optional): Starting index for pagination (default: 0)
- `limit` (int, optional): Maximum results to return (default: 25)

**Returns:** List of dictionaries containing skater statistics.

**Example:**
```python
from nhl_api import get_nhl_skater_stats_summary

result = get_nhl_skater_stats_summary("20232024", "20232024", limit=10)
if "skater_stats" in result:
    for skater in result["skater_stats"]:
        print(f"{skater['skaterFullName']}: {skater['points']} points")
```

### 6. Goalie Stats Summary

**Function:** `get_nhl_goalie_stats_summary(start_season, end_season, stats_type, game_type_id, franchise_id, aggregate, start, limit)`

**Description:** Retrieves goalie statistics with various filtering and aggregation options.

**Parameters:**
- `start_season` (str): Beginning season in YYYYYYYY format
- `end_season` (str, optional): Ending season (defaults to start_season)
- `stats_type` (str): Type of statistics to retrieve (default: "summary")
- `game_type_id` (int, optional): Game type (default: 2 for regular season)
- `franchise_id` (str, optional): Franchise identifier for filtering
- `aggregate` (bool, optional): Combine multiple seasons per goalie (default: False)
- `start` (int, optional): Starting index for pagination (default: 0)
- `limit` (int, optional): Maximum results to return (default: 25)

**Available Stats Types:**
- `summary`: Basic goalie statistics
- `advanced`: Advanced goalie metrics
- `bios`: Biographical information
- `daysrest`: Performance by days of rest
- `penaltyShots`: Penalty shot statistics
- `savesByStrength`: Save performance by game situation
- `shootout`: Shootout statistics
- `startedVsRelieved`: Starter vs reliever performance

**Returns:** List of dictionaries containing goalie statistics.

**Example:**
```python
from nhl_api import get_nhl_goalie_stats_summary

result = get_nhl_goalie_stats_summary("20242025", "20242025", "summary", limit=10)
if "goalie_stats" in result:
    for goalie in result["goalie_stats"]:
        print(f"{goalie['goalieFullName']}: {goalie['wins']}W-{goalie['losses']}L")
```

## MCP Server Integration

All Stats API functions are also available as MCP tools with the `_mcp` suffix:

- `get_nhl_gametypes_per_season_by_team_mcp`
- `get_nhl_player_career_stats_mcp`
- `get_nhl_player_game_log_mcp`
- `get_nhl_team_summary_stats_mcp`
- `get_nhl_skater_stats_summary_mcp`
- `get_nhl_goalie_stats_summary_mcp`

## Error Handling

All functions include comprehensive error handling and return consistent response formats:

**Success Response:**
```json
{
  "data_key": [actual_data_here]
}
```

**Error Response:**
```json
{
  "error": "Error message description"
}
```

## Usage Examples

See `example_stats_usage.py` for comprehensive examples of how to use each Stats API function.

## Testing

The Stats API functions include comprehensive unit tests in `tests/test_nhl_api.py`. Run the tests with:

```bash
python -m pytest tests/test_nhl_api.py -v
```

## Dependencies

- `nhlpy`: NHL API Python wrapper
- `pytest`: For running tests (development dependency)

## Notes

- All season parameters use the YYYYYYYY format (e.g., "20242025" for 2024-2025 season)
- Game type IDs are consistent across all functions (1=Preseason, 2=Regular, 3=Playoffs)
- Franchise IDs are different from team IDs and are specific to the /stats APIs
- The API includes built-in pagination support with `start` and `limit` parameters
- All functions support both single-season and multi-season queries
