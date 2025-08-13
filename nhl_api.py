from nhlpy import NHLClient

client = NHLClient(debug=True)

def get_nhl_teams_direct() -> dict:
    """
    Get all NHL teams directly (for testing purposes).
    
    Returns:
        dict: All NHL teams with their information.
    """
    try:
        teams = client.teams.teams()
        return {"teams": teams}
    except Exception as e:
        return {"error": str(e)}

def setup_nhl_tools(mcp):
    """Setup NHL tools for the MCP server"""
    
    @mcp.tool()
    def get_nhl_teams() -> dict:
        """
        Get all NHL teams.
        
        Returns:
            dict: All NHL teams with their information.
        """
        try:
            teams = client.teams.teams()
            return {"teams": teams}
        except Exception as e:
            return {"error": str(e)}



