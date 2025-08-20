import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import nhl_api
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nhl_api import setup_nhl_tools, client


class TestNHLAPI:
    """Test cases for NHL API functionality"""
    
    def test_client_initialization(self):
        """Test that NHL client is properly initialized"""
        assert client is not None
        assert hasattr(client, 'teams')
    
    @patch('nhl_api.client.teams.teams')
    def test_get_nhl_teams_success(self, mock_teams):
        """Test successful retrieval of NHL teams"""
        # Mock the teams response
        mock_teams.return_value = [
            {
                "name": "Boston Bruins",
                "abbr": "BOS",
                "conference": {"abbr": "EAST", "name": "Eastern"},
                "division": {"abbr": "ATL", "name": "Atlantic"}
            },
            {
                "name": "Toronto Maple Leafs",
                "abbr": "TOR",
                "conference": {"abbr": "EAST", "name": "Eastern"},
                "division": {"abbr": "ATL", "name": "Atlantic"}
            }
        ]
        
        # Test the function directly by importing and calling it
        from nhl_api import get_nhl_teams
        result = get_nhl_teams()
        
        # Verify the result
        assert "teams" in result
        assert len(result["teams"]) == 2
        assert result["teams"][0]["name"] == "Boston Bruins"
        assert result["teams"][0]["abbr"] == "BOS"
        assert result["teams"][1]["conference"]["abbr"] == "EAST"
        
        # Verify the mock was called with default parameter
        mock_teams.assert_called_once_with("now")
    
    @patch('nhl_api.client.teams.teams')
    def test_get_nhl_teams_with_date(self, mock_teams):
        """Test successful retrieval of NHL teams with specific date"""
        # Mock the teams response
        mock_teams.return_value = [
            {
                "name": "Boston Bruins",
                "abbr": "BOS",
                "conference": {"abbr": "EAST", "name": "Eastern"}
            }
        ]
        
        # Test the function directly by importing and calling it
        from nhl_api import get_nhl_teams
        result = get_nhl_teams(date="2024-10-04")
        
        # Verify the result
        assert "teams" in result
        assert len(result["teams"]) == 1
        
        # Verify the mock was called with the specified date
        mock_teams.assert_called_once_with("2024-10-04")
    
    @patch('nhl_api.client.teams.teams')
    def test_get_nhl_teams_error(self, mock_teams):
        """Test error handling when NHL teams API fails"""
        # Mock the teams response to raise an exception
        mock_teams.side_effect = Exception("API Error")
        
        # Test the function directly by importing and calling it
        from nhl_api import get_nhl_teams
        result = get_nhl_teams()
        
        # Verify the error result
        assert "error" in result
        assert result["error"] == "API Error"
    
    @patch('nhl_api.client.teams.team_roster')
    def test_get_nhl_team_roster_success(self, mock_roster):
        """Test successful retrieval of team roster"""
        # Mock the roster response
        mock_roster.return_value = {
            "roster": [
                {"id": 1, "name": "Jack Hughes", "position": "C", "number": "86"},
                {"id": 2, "name": "Nico Hischier", "position": "C", "number": "13"}
            ]
        }
        
        # Test the function directly by importing and calling it
        from nhl_api import get_nhl_team_roster
        result = get_nhl_team_roster(team_abbr="NJD", season="20232024")
        
        # Verify the result
        assert "roster" in result
        assert "roster" in result["roster"]
        assert len(result["roster"]["roster"]) == 2
        assert result["roster"]["roster"][0]["name"] == "Jack Hughes"
        assert result["roster"]["roster"][1]["position"] == "C"
        
        # Verify the mock was called with correct parameters
        mock_roster.assert_called_once_with("NJD", "20232024")
    
    @patch('nhl_api.client.teams.team_roster')
    def test_get_nhl_team_roster_error(self, mock_roster):
        """Test error handling when getting team roster fails"""
        # Mock the roster response to raise an exception
        mock_roster.side_effect = Exception("Team not found")
        
        # Test the function directly by importing and calling it
        from nhl_api import get_nhl_team_roster
        result = get_nhl_team_roster(team_abbr="INVALID", season="20232024")
        
        # Verify the error result
        assert "error" in result
        assert result["error"] == "Team not found"
    
    @patch('nhl_api.client.teams.franchises')
    def test_get_nhl_franchises_success(self, mock_franchises):
        """Test successful retrieval of NHL franchises"""
        # Mock the franchises response
        mock_franchises.return_value = [
            {"id": 1, "fullName": "Boston Bruins", "active": True},
            {"id": 2, "fullName": "Toronto Maple Leafs", "active": True},
            {"id": 3, "fullName": "Montreal Canadiens", "active": True}
        ]
        
        # Test the function directly by importing and calling it
        from nhl_api import get_nhl_franchises
        result = get_nhl_franchises()
        
        # Verify the result
        assert "franchises" in result
        assert len(result["franchises"]) == 3
        assert result["franchises"][0]["fullName"] == "Boston Bruins"
        assert result["franchises"][1]["active"] == True
        
        # Verify the mock was called
        mock_franchises.assert_called_once()
    
    @patch('nhl_api.client.teams.franchises')
    def test_get_nhl_franchises_error(self, mock_franchises):
        """Test error handling when getting franchises fails"""
        # Mock the franchises response to raise an exception
        mock_franchises.side_effect = Exception("Franchises API error")
        
        # Test the function directly by importing and calling it
        from nhl_api import get_nhl_franchises
        result = get_nhl_franchises()
        
        # Verify the error result
        assert "error" in result
        assert result["error"] == "Franchises API error"
    
    @patch('nhl_api.client.teams.teams')
    def test_get_nhl_team_ids_success(self, mock_teams):
        """Test successful retrieval of team abbreviation mapping"""
        # Mock the teams response
        mock_teams.return_value = [
            {"name": "Boston Bruins", "abbr": "BOS"},
            {"name": "Toronto Maple Leafs", "abbr": "TOR"},
            {"name": "New Jersey Devils", "abbr": "NJD"}
        ]
        
        # Test the function directly by importing and calling it
        from nhl_api import get_nhl_team_ids
        result = get_nhl_team_ids()
        
        # Verify the result
        assert "team_abbreviations" in result
        assert result["team_abbreviations"]["Boston Bruins"] == "BOS"
        assert result["team_abbreviations"]["Toronto Maple Leafs"] == "TOR"
        assert result["team_abbreviations"]["New Jersey Devils"] == "NJD"
        
        # Verify the mock was called
        mock_teams.assert_called_once_with("now")
    
    def test_setup_nhl_tools_registers_all_tools(self):
        """Test that setup_nhl_tools properly registers all tools with MCP"""
        mock_mcp = Mock()
        
        # Setup the tools
        setup_nhl_tools(mock_mcp)
        
        # Verify that the tool decorator was called 4 times (4 tools total)
        assert mock_mcp.tool.call_count == 4
        
        # Verify the tool names are registered
        tool_calls = mock_mcp.tool.call_args_list
        assert len(tool_calls) == 4


if __name__ == "__main__":
    pytest.main([__file__])
