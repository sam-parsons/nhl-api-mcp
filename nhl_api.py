from nhlpy import NHLClient

client = NHLClient(debug=True)

def get_nhl_teams(date: str = "now") -> dict:
    """
    Get all NHL teams with conference, division, and franchise information.
    
    Args:
        date: Date in format YYYY-MM-DD. Defaults to "now".
            Note: During preseason, "now" may default to last year's season.
            For accurate current season teams, supply a date at season start.
            Examples: "2024-04-18" for 2023-2024, "2024-10-04" for 2024-2025
    
    Returns:
        dict: All NHL teams with their information.
    """
    try:
        teams = client.teams.teams(date)
        return {"teams": teams}
    except Exception as e:
        return {"error": str(e)}

def get_nhl_team_roster(team_abbr: str, season: str) -> dict:
    """
    Get the roster for a specific NHL team and season.
    
    Args:
        team_abbr: Team abbreviation (e.g., BUF, TOR, BOS)
        season: Season in format YYYYYYYY (e.g., 20232024, 20242025)
        
    Returns:
        dict: Team roster or error message.
    """
    try:
        roster = client.teams.team_roster(team_abbr, season)
        return {"roster": roster}
    except Exception as e:
        return {"error": str(e)}

def get_nhl_franchises() -> dict:
    """
    Get a list of all past and current NHL franchises.
    
    Returns:
        dict: All NHL franchises including historical/defunct teams.
    """
    try:
        franchises = client.teams.franchises()
        return {"franchises": franchises}
    except Exception as e:
        return {"error": str(e)}

def get_nhl_team_ids(date: str = "now") -> dict:
    """
    Get a mapping of NHL team names to their abbreviations for reference.
    
    Args:
        date: Date in format YYYY-MM-DD. Defaults to "now".
            Note: During preseason, "now" may default to last year's season.
            For accurate current season teams, supply a date at season start.
    
    Returns:
        dict: Dictionary mapping team names to abbreviations or error message.
    """
    try:
        teams = client.teams.teams(date)
        team_mapping = {team.get('name', 'Unknown'): team.get('abbr', 'Unknown') for team in teams}
        return {"team_abbreviations": team_mapping}
    except Exception as e:
        return {"error": str(e)}

def get_nhl_standings(date: str = "now", season: str = None) -> dict:
    """
    Get NHL league standings for a specified season or date.
    
    Retrieves NHL standings either for a specific date or for the end of a season.
    If both parameters are provided, season takes precedence.
    
    Args:
        date: Date in YYYY-MM-DD format. Defaults to current date.
        season: Season identifier to get final standings (e.g., 20232024, 20242025).
               Takes precedence over date parameter if both are provided.
    
    Returns:
        dict: League standings data or error message.
    """
    try:
        # If season is provided, we need to look up the last date of the season
        if season:
            seasons_response = get_nhl_season_manifest()
            if "error" in seasons_response:
                return seasons_response
            seasons = seasons_response.get("seasons", [])
            season_data = next((s for s in seasons if s.get("id") == int(season)), None)
            if not season_data:
                raise ValueError(f"Invalid Season Id {season}")
            date = season_data.get("standingsEnd")
        
        res = date if date else "now"
        standings = client.standings.league_standings(res)
        return {"standings": standings}
    except Exception as e:
        return {"error": str(e)}

def get_nhl_season_manifest() -> dict:
    """
    Get metadata for all NHL seasons.
    
    Returns information about every season including start/end dates, 
    conference/division usage, and scoring rules.
    
    Returns:
        dict: Season metadata or error message.
        
    Example response format:
    [{
        "id": 20232024,
        "conferencesInUse": true,
        "divisionsInUse": true,
        "pointForOTlossInUse": true,
        "regulationWinsInUse": true,
        "rowInUse": true,
        "standingsEnd": "2023-11-10",
        "standingsStart": "2023-10-10",
        "tiesInUse": false,
        "wildcardInUse": true
    }]
    """
    try:
        seasons = client.standings.season_standing_manifest()
        return {"seasons": seasons}
    except Exception as e:
        return {"error": str(e)}

def setup_nhl_tools(mcp):
    """Setup NHL tools for the MCP server"""
    
    @mcp.tool()
    def get_nhl_teams_mcp(date: str = "now") -> dict:
        return get_nhl_teams(date)

    @mcp.tool()
    def get_nhl_team_roster_mcp(team_abbr: str, season: str) -> dict:
        return get_nhl_team_roster(team_abbr, season)

    @mcp.tool()
    def get_nhl_franchises_mcp() -> dict:
        return get_nhl_franchises()

    @mcp.tool()
    def get_nhl_team_ids_mcp() -> dict:
        return get_nhl_team_ids()

    @mcp.tool()
    def get_nhl_standings_mcp(date: str = "now", season: str = None) -> dict:
        return get_nhl_standings(date, season)

    @mcp.tool()
    def get_nhl_season_manifest_mcp() -> dict:
        return get_nhl_season_manifest()



