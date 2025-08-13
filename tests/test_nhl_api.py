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
            {"id": 1, "name": "Boston Bruins", "abbreviation": "BOS"},
            {"id": 2, "name": "Toronto Maple Leafs", "abbreviation": "TOR"}
        ]
        
        # Test the function directly without MCP wrapper
        from nhl_api import get_nhl_teams_direct
        
        # Call the function directly
        result = get_nhl_teams_direct()
        
        # Verify the result
        assert "teams" in result
        assert len(result["teams"]) == 2
        assert result["teams"][0]["name"] == "Boston Bruins"
        assert result["teams"][1]["abbreviation"] == "TOR"
        
        # Verify the mock was called
        mock_teams.assert_called_once()
    
    @patch('nhl_api.client.teams.teams')
    def test_get_nhl_teams_error(self, mock_teams):
        """Test error handling when NHL teams API fails"""
        # Mock the teams response to raise an exception
        mock_teams.side_effect = Exception("API Error")
        
        # Test the function directly without MCP wrapper
        from nhl_api import get_nhl_teams_direct
        
        # Call the function directly
        result = get_nhl_teams_direct()
        
        # Verify the error result
        assert "error" in result
        assert result["error"] == "API Error"
    
    def test_setup_nhl_tools_registers_tool(self):
        """Test that setup_nhl_tools properly registers the tool with MCP"""
        mock_mcp = Mock()
        
        # Setup the tools
        setup_nhl_tools(mock_mcp)
        
        # Verify that the tool decorator was called
        mock_mcp.tool.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])
