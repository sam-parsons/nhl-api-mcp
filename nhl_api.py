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

def get_nhl_prospects_by_team(team_abbr: str) -> dict:
    """
    Get prospects for a specific NHL team.
    
    Args:
        team_abbr: Team abbreviation (e.g., BUF, TOR, BOS)
        
    Returns:
        dict: Prospects data for the specified team or error message.
    """
    try:
        prospects = client.players.prospects_by_team(team_abbr)
        return {"prospects": prospects}
    except Exception as e:
        return {"error": str(e)}

def get_nhl_players_by_team(team_abbr: str, season: str) -> dict:
    """
    Get the roster/players for the given team and season.
    
    This method provides the same functionality as get_nhl_team_roster(),
    offering a convenient way to access team rosters through the Players API.
    
    Args:
        team_abbr: Team abbreviation (e.g., BUF, TOR, BOS)
        season: Season in format YYYYYYYY (e.g., 20232024, 20242025)
        
    Returns:
        dict: Dictionary containing roster information for the specified team and season or error message.
    """
    try:
        players = client.players.players_by_team(team_abbr, season)
        return {"players": players}
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

def get_nhl_daily_schedule(date: str = None) -> dict:
    """
    Get NHL schedule for a specific date.
    
    Args:
        date: Date in YYYY-MM-DD format. Defaults to today's date.
    
    Returns:
        dict: Game schedule data for the specified date or error message.
    """
    try:
        from datetime import datetime
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")  # Default to today's date
        else:
            # Parse and reformat the date to ensure YYYY-MM-DD
            date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        
        schedule_data = client.schedule.daily_schedule(date)
        return {"schedule": schedule_data}
    except ValueError as e:
        return {"error": f"Invalid date format: {str(e)}. Please use YYYY-MM-DD."}
    except Exception as e:
        return {"error": str(e)}

def get_nhl_weekly_schedule(date: str = None) -> dict:
    """
    Get NHL schedule for a week starting from the specified date.
    
    Args:
        date: Date in YYYY-MM-DD format. Defaults to today's date.
              Note: NHL's "today" typically shifts around 12:00 EST.
    
    Returns:
        dict: Weekly game schedule data or error message.
    """
    try:
        res = date if date else "now"
        schedule = client.schedule.weekly_schedule(res)
        return {"schedule": schedule}
    except Exception as e:
        return {"error": str(e)}

def get_nhl_team_monthly_schedule(team_abbr: str, month: str = None) -> dict:
    """
    Get monthly schedule for specified team or the given month.
    
    Args:
        team_abbr: Three-letter team abbreviation (e.g., BUF, TOR)
        month: Month in YYYY-MM format (e.g., 2021-10). Defaults to current month.
    
    Returns:
        dict: Monthly schedule data or error message.
    """
    try:
        games = client.schedule.team_monthly_schedule(team_abbr, month)
        return {"games": games, "team": team_abbr, "month": month}
    except Exception as e:
        return {"error": str(e)}

def get_nhl_team_weekly_schedule(team_abbr: str, date: str = None) -> dict:
    """
    Get weekly schedule for specified team.
    
    Args:
        team_abbr: Three-letter team abbreviation (e.g., BUF, TOR)
        date: Date in YYYY-MM-DD format. Gets schedule for week containing this date.
              Defaults to current week.
    
    Returns:
        dict: Weekly schedule data or error message.
    """
    try:
        games = client.schedule.team_weekly_schedule(team_abbr, date)
        return {"games": games, "team": team_abbr, "date": date}
    except Exception as e:
        return {"error": str(e)}

def get_nhl_team_season_schedule(team_abbr: str, season: str) -> dict:
    """
    Get full season schedule for specified team.
    
    Args:
        team_abbr: Three-letter team abbreviation (e.g., BUF, TOR)
        season: Season in YYYYYYYY format (e.g., 20232024)
    
    Returns:
        dict: Complete season schedule data including metadata or error message.
    """
    try:
        schedule = client.schedule.team_season_schedule(team_abbr, season)
        return {"schedule": schedule, "team": team_abbr, "season": season}
    except Exception as e:
        return {"error": str(e)}

def get_nhl_calendar_schedule(date: str) -> dict:
    """
    Get schedule in calendar format for specified date.
    
    Args:
        date: Date in YYYY-MM-DD format (e.g., 2023-11-23)
    
    Returns:
        dict: Calendar-formatted schedule data or error message.
    """
    try:
        schedule = client.schedule.calendar_schedule(date)
        return {"schedule": schedule, "date": date}
    except Exception as e:
        return {"error": str(e)}

def get_nhl_playoff_carousel(season: str) -> dict:
    """
    Get list of all series games up to current playoff round.
    
    Args:
        season: Season in YYYYYYYY format (e.g., "20232024")
    
    Returns:
        dict: Playoff series data for the specified season or error message.
    """
    try:
        playoff_data = client.schedule.playoff_carousel(season)
        return {"playoff_data": playoff_data, "season": season}
    except Exception as e:
        return {"error": str(e)}

def get_nhl_playoff_series_schedule(season: str, series: str) -> dict:
    """
    Get the schedule for a specified playoff series.
    
    Args:
        season: Season in YYYYYYYY format (e.g., "20232024")
        series: Series identifier (a-h) for Round 1
    
    Returns:
        dict: Schedule data for the specified playoff series or error message.
    """
    try:
        series_schedule = client.schedule.playoff_series_schedule(season, series)
        return {"series_schedule": series_schedule, "season": season, "series": series}
    except Exception as e:
        return {"error": str(e)}

def get_nhl_playoff_bracket(year: str) -> dict:
    """
    Get the playoff bracket.
    
    Args:
        year: Year playoffs take place (e.g., "2024")
    
    Returns:
        dict: Playoff bracket data or error message.
    """
    try:
        bracket = client.schedule.playoff_bracket(year)
        return {"bracket": bracket, "year": year}
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
    def get_nhl_prospects_by_team_mcp(team_abbr: str) -> dict:
        return get_nhl_prospects_by_team(team_abbr)

    @mcp.tool()
    def get_nhl_players_by_team_mcp(team_abbr: str, season: str) -> dict:
        return get_nhl_players_by_team(team_abbr, season)

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

    @mcp.tool()
    def get_nhl_daily_schedule_mcp(date: str = None) -> dict:
        return get_nhl_daily_schedule(date)

    @mcp.tool()
    def get_nhl_weekly_schedule_mcp(date: str = None) -> dict:
        return get_nhl_weekly_schedule(date)

    @mcp.tool()
    def get_nhl_team_monthly_schedule_mcp(team_abbr: str, month: str = None) -> dict:
        return get_nhl_team_monthly_schedule(team_abbr, month)

    @mcp.tool()
    def get_nhl_team_weekly_schedule_mcp(team_abbr: str, date: str = None) -> dict:
        return get_nhl_team_weekly_schedule(team_abbr, date)

    @mcp.tool()
    def get_nhl_team_season_schedule_mcp(team_abbr: str, season: str) -> dict:
        return get_nhl_team_season_schedule(team_abbr, season)

    @mcp.tool()
    def get_nhl_calendar_schedule_mcp(date: str) -> dict:
        return get_nhl_calendar_schedule(date)

    @mcp.tool()
    def get_nhl_playoff_carousel_mcp(season: str) -> dict:
        return get_nhl_playoff_carousel(season)

    @mcp.tool()
    def get_nhl_playoff_series_schedule_mcp(season: str, series: str) -> dict:
        return get_nhl_playoff_series_schedule(season, series)

    @mcp.tool()
    def get_nhl_playoff_bracket_mcp(year: str) -> dict:
        return get_nhl_playoff_bracket(year)



