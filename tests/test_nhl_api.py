import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nhl_api import setup_nhl_tools, client


class TestNHLAPI:
    
    def test_client_initialization(self):
        assert client is not None
        assert hasattr(client, 'teams')
        assert hasattr(client, 'standings')
        assert hasattr(client, 'schedule')
    
    @patch('nhl_api.client.teams.teams')
    def test_get_nhl_teams_success(self, mock_teams):
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
        
        from nhl_api import get_nhl_teams
        result = get_nhl_teams()
        
        assert "teams" in result
        assert len(result["teams"]) == 2
        assert result["teams"][0]["name"] == "Boston Bruins"
        assert result["teams"][0]["abbr"] == "BOS"
        assert result["teams"][1]["conference"]["abbr"] == "EAST"
        
        mock_teams.assert_called_once_with("now")
    
    @patch('nhl_api.client.teams.teams')
    def test_get_nhl_teams_with_date(self, mock_teams):
        mock_teams.return_value = [
            {
                "name": "Boston Bruins",
                "abbr": "BOS",
                "conference": {"abbr": "EAST", "name": "Eastern"}
            }
        ]
        
        from nhl_api import get_nhl_teams
        result = get_nhl_teams(date="2024-10-04")
        
        assert "teams" in result
        assert len(result["teams"]) == 1
        
        mock_teams.assert_called_once_with("2024-10-04")
    
    @patch('nhl_api.client.teams.teams')
    def test_get_nhl_teams_error(self, mock_teams):
        mock_teams.side_effect = Exception("API Error")
        
        from nhl_api import get_nhl_teams
        result = get_nhl_teams()
        
        assert "error" in result
        assert result["error"] == "API Error"
    
    @patch('nhl_api.client.teams.team_roster')
    def test_get_nhl_team_roster_success(self, mock_roster):
        mock_roster.return_value = {
            "roster": [
                {"id": 1, "name": "Jack Hughes", "position": "C", "number": "86"},
                {"id": 2, "name": "Nico Hischier", "position": "C", "number": "13"}
            ]
        }
        
        from nhl_api import get_nhl_team_roster
        result = get_nhl_team_roster(team_abbr="NJD", season="20232024")
        
        assert "roster" in result
        assert "roster" in result["roster"]
        assert len(result["roster"]["roster"]) == 2
        assert result["roster"]["roster"][0]["name"] == "Jack Hughes"
        assert result["roster"]["roster"][1]["position"] == "C"
        
        mock_roster.assert_called_once_with("NJD", "20232024")
    
    @patch('nhl_api.client.teams.team_roster')
    def test_get_nhl_team_roster_error(self, mock_roster):
        mock_roster.side_effect = Exception("Team not found")
        
        from nhl_api import get_nhl_team_roster
        result = get_nhl_team_roster(team_abbr="INVALID", season="20232024")
        
        assert "error" in result
        assert result["error"] == "Team not found"
    
    @patch('nhl_api.client.players.prospects_by_team')
    def test_get_nhl_prospects_by_team_success(self, mock_prospects):
        mock_prospects.return_value = {
            "prospects": [
                {"id": 1, "name": "Connor Bedard", "position": "C", "draftYear": 2023},
                {"id": 2, "name": "Adam Fantilli", "position": "C", "draftYear": 2023}
            ]
        }
        
        from nhl_api import get_nhl_prospects_by_team
        result = get_nhl_prospects_by_team(team_abbr="CHI")
        
        assert "prospects" in result
        assert "prospects" in result["prospects"]
        assert len(result["prospects"]["prospects"]) == 2
        assert result["prospects"]["prospects"][0]["name"] == "Connor Bedard"
        assert result["prospects"]["prospects"][1]["position"] == "C"
        
        mock_prospects.assert_called_once_with("CHI")
    
    @patch('nhl_api.client.players.prospects_by_team')
    def test_get_nhl_prospects_by_team_error(self, mock_prospects):
        mock_prospects.side_effect = Exception("Prospects API error")
        
        from nhl_api import get_nhl_prospects_by_team
        result = get_nhl_prospects_by_team(team_abbr="INVALID")
        
        assert "error" in result
        assert result["error"] == "Prospects API error"
    
    @patch('nhl_api.client.players.players_by_team')
    def test_get_nhl_players_by_team_success(self, mock_players):
        mock_players.return_value = {
            "roster": [
                {"id": 1, "name": "Jack Hughes", "position": "C", "number": "86"},
                {"id": 2, "name": "Nico Hischier", "position": "C", "number": "13"}
            ]
        }
        
        from nhl_api import get_nhl_players_by_team
        result = get_nhl_players_by_team(team_abbr="NJD", season="20232024")
        
        assert "players" in result
        assert "roster" in result["players"]
        assert len(result["players"]["roster"]) == 2
        assert result["players"]["roster"][0]["name"] == "Jack Hughes"
        assert result["players"]["roster"][1]["position"] == "C"
        
        mock_players.assert_called_once_with("NJD", "20232024")
    
    @patch('nhl_api.client.players.players_by_team')
    def test_get_nhl_players_by_team_error(self, mock_players):
        mock_players.side_effect = Exception("Players API error")
        
        from nhl_api import get_nhl_players_by_team
        result = get_nhl_players_by_team(team_abbr="INVALID", season="20232024")
        
        assert "error" in result
        assert result["error"] == "Players API error"
    
    @patch('nhl_api.client.teams.franchises')
    def test_get_nhl_franchises_success(self, mock_franchises):
        mock_franchises.return_value = [
            {"id": 1, "fullName": "Boston Bruins", "active": True},
            {"id": 2, "fullName": "Toronto Maple Leafs", "active": True},
            {"id": 3, "fullName": "Montreal Canadiens", "active": True}
        ]
        
        from nhl_api import get_nhl_franchises
        result = get_nhl_franchises()
        
        assert "franchises" in result
        assert len(result["franchises"]) == 3
        assert result["franchises"][0]["fullName"] == "Boston Bruins"
        assert result["franchises"][1]["active"] == True
        
        mock_franchises.assert_called_once()
    
    @patch('nhl_api.client.teams.franchises')
    def test_get_nhl_franchises_error(self, mock_franchises):
        mock_franchises.side_effect = Exception("Franchises API error")
        
        from nhl_api import get_nhl_franchises
        result = get_nhl_franchises()
        
        assert "error" in result
        assert result["error"] == "Franchises API error"
    
    @patch('nhl_api.client.teams.teams')
    def test_get_nhl_team_ids_success(self, mock_teams):
        mock_teams.return_value = [
            {"name": "Boston Bruins", "abbr": "BOS"},
            {"name": "Toronto Maple Leafs", "abbr": "TOR"},
            {"name": "New Jersey Devils", "abbr": "NJD"}
        ]
        
        from nhl_api import get_nhl_team_ids
        result = get_nhl_team_ids()
        
        assert "team_abbreviations" in result
        assert result["team_abbreviations"]["Boston Bruins"] == "BOS"
        assert result["team_abbreviations"]["Toronto Maple Leafs"] == "TOR"
        assert result["team_abbreviations"]["New Jersey Devils"] == "NJD"
        
        mock_teams.assert_called_once_with("now")
    
    @patch('nhl_api.client.standings.league_standings')
    def test_get_nhl_standings_success(self, mock_standings):
        mock_standings.return_value = {
            "standings": [
                {"team": "Boston Bruins", "points": 100, "wins": 45},
                {"team": "Toronto Maple Leafs", "points": 95, "wins": 42}
            ]
        }
        
        from nhl_api import get_nhl_standings
        result = get_nhl_standings()
        
        assert "standings" in result
        assert "standings" in result["standings"]
        assert len(result["standings"]["standings"]) == 2
        assert result["standings"]["standings"][0]["team"] == "Boston Bruins"
        assert result["standings"]["standings"][1]["points"] == 95
        
        mock_standings.assert_called_once_with("now")
    
    @patch('nhl_api.client.standings.league_standings')
    def test_get_nhl_standings_with_date(self, mock_standings):
        mock_standings.return_value = {
            "standings": [
                {"team": "Boston Bruins", "points": 100, "wins": 45}
            ]
        }
        
        from nhl_api import get_nhl_standings
        result = get_nhl_standings(date="2024-01-15")
        
        assert "standings" in result
        assert "standings" in result["standings"]
        assert len(result["standings"]["standings"]) == 1
        
        mock_standings.assert_called_once_with("2024-01-15")
    
    @patch('nhl_api.client.standings.league_standings')
    @patch('nhl_api.get_nhl_season_manifest')
    def test_get_nhl_standings_with_season(self, mock_season_manifest, mock_standings):
        mock_season_manifest.return_value = {
            "seasons": [
                {
                    "id": 20232024,
                    "standingsEnd": "2024-04-18",
                    "conferencesInUse": True,
                    "divisionsInUse": True
                }
            ]
        }
        
        mock_standings.return_value = {
            "standings": [
                {"team": "Boston Bruins", "points": 100, "wins": 45}
            ]
        }
        
        from nhl_api import get_nhl_standings
        result = get_nhl_standings(season="20232024")
        
        assert "standings" in result
        assert "standings" in result["standings"]
        assert len(result["standings"]["standings"]) == 1
        
        mock_standings.assert_called_once_with("2024-04-18")
    
    @patch('nhl_api.client.standings.league_standings')
    @patch('nhl_api.get_nhl_season_manifest')
    def test_get_nhl_standings_invalid_season(self, mock_season_manifest, mock_standings):
        mock_season_manifest.return_value = {
            "seasons": [
                {
                    "id": 20232024,
                    "standingsEnd": "2024-04-18"
                }
            ]
        }
        
        from nhl_api import get_nhl_standings
        result = get_nhl_standings(season="99999999")
        
        assert "error" in result
        assert "Invalid Season Id 99999999" in result["error"]
    
    @patch('nhl_api.client.standings.league_standings')
    def test_get_nhl_standings_error(self, mock_standings):
        mock_standings.side_effect = Exception("Standings API error")
        
        from nhl_api import get_nhl_standings
        result = get_nhl_standings()
        
        assert "error" in result
        assert result["error"] == "Standings API error"
    
    @patch('nhl_api.client.standings.season_standing_manifest')
    def test_get_nhl_season_manifest_success(self, mock_season_manifest):
        mock_season_manifest.return_value = [
            {
                "id": 20232024,
                "conferencesInUse": True,
                "divisionsInUse": True,
                "pointForOTlossInUse": True,
                "regulationWinsInUse": True,
                "rowInUse": True,
                "standingsEnd": "2024-04-18",
                "standingsStart": "2023-10-10",
                "tiesInUse": False,
                "wildcardInUse": True
            },
            {
                "id": 20242025,
                "conferencesInUse": True,
                "divisionsInUse": True,
                "pointForOTlossInUse": True,
                "regulationWinsInUse": True,
                "rowInUse": True,
                "standingsEnd": "2025-04-17",
                "standingsStart": "2024-10-08",
                "tiesInUse": False,
                "wildcardInUse": True
            }
        ]
        
        from nhl_api import get_nhl_season_manifest
        result = get_nhl_season_manifest()
        
        assert "seasons" in result
        assert len(result["seasons"]) == 2
        assert result["seasons"][0]["id"] == 20232024
        assert result["seasons"][0]["standingsEnd"] == "2024-04-18"
        assert result["seasons"][1]["id"] == 20242025
        assert result["seasons"][1]["standingsStart"] == "2024-10-08"
        
        mock_season_manifest.assert_called_once()
    
    @patch('nhl_api.client.standings.season_standing_manifest')
    def test_get_nhl_season_manifest_error(self, mock_season_manifest):
        mock_season_manifest.side_effect = Exception("Season manifest API error")
        
        from nhl_api import get_nhl_season_manifest
        result = get_nhl_season_manifest()
        
        assert "error" in result
        assert result["error"] == "Season manifest API error"
    
    @patch('nhl_api.client.schedule.daily_schedule')
    def test_get_nhl_daily_schedule_success(self, mock_daily_schedule):
        mock_daily_schedule.return_value = {
            "nextStartDate": "2024-01-16",
            "previousStartDate": "2024-01-14",
            "date": "2024-01-15",
            "oddsPartners": ["partner1", "partner2"],
            "games": [
                {"id": 1, "homeTeam": "BOS", "awayTeam": "TOR", "startTime": "19:00"},
                {"id": 2, "homeTeam": "NJD", "awayTeam": "NYR", "startTime": "19:30"}
            ],
            "numberOfGames": 2
        }
        
        from nhl_api import get_nhl_daily_schedule
        result = get_nhl_daily_schedule("2024-01-15")
        
        assert "schedule" in result
        assert result["schedule"]["date"] == "2024-01-15"
        assert result["schedule"]["numberOfGames"] == 2
        assert len(result["schedule"]["games"]) == 2
        
        mock_daily_schedule.assert_called_once_with("2024-01-15")
    
    @patch('nhl_api.client.schedule.daily_schedule')
    def test_get_nhl_daily_schedule_default_date(self, mock_daily_schedule):
        mock_daily_schedule.return_value = {
            "date": "2024-01-15",
            "games": [],
            "numberOfGames": 0
        }
        
        from nhl_api import get_nhl_daily_schedule
        result = get_nhl_daily_schedule()
        
        assert "schedule" in result
        assert "date" in result["schedule"]
        
        mock_daily_schedule.assert_called_once()
    
    def test_get_nhl_daily_schedule_invalid_date_format(self):
        from nhl_api import get_nhl_daily_schedule
        result = get_nhl_daily_schedule("invalid-date")
        
        assert "error" in result
        assert "Invalid date format" in result["error"]
    
    @patch('nhl_api.client.schedule.daily_schedule')
    def test_get_nhl_daily_schedule_error(self, mock_daily_schedule):
        mock_daily_schedule.side_effect = Exception("Daily schedule API error")
        
        from nhl_api import get_nhl_daily_schedule
        result = get_nhl_daily_schedule("2024-01-15")
        
        assert "error" in result
        assert result["error"] == "Daily schedule API error"
    
    @patch('nhl_api.client.schedule.weekly_schedule')
    def test_get_nhl_weekly_schedule_success(self, mock_weekly_schedule):
        mock_weekly_schedule.return_value = {
            "gameWeek": [
                {"date": "2024-01-15", "games": [{"id": 1, "homeTeam": "BOS"}]},
                {"date": "2024-01-16", "games": [{"id": 2, "homeTeam": "TOR"}]}
            ]
        }
        
        from nhl_api import get_nhl_weekly_schedule
        result = get_nhl_weekly_schedule("2024-01-15")
        
        assert "schedule" in result
        assert "gameWeek" in result["schedule"]
        assert len(result["schedule"]["gameWeek"]) == 2
        
        mock_weekly_schedule.assert_called_once_with("2024-01-15")
    
    @patch('nhl_api.client.schedule.weekly_schedule')
    def test_get_nhl_weekly_schedule_default_date(self, mock_weekly_schedule):
        mock_weekly_schedule.return_value = {"gameWeek": []}
        
        from nhl_api import get_nhl_weekly_schedule
        result = get_nhl_weekly_schedule()
        
        assert "schedule" in result
        
        mock_weekly_schedule.assert_called_once_with("now")
    
    @patch('nhl_api.client.schedule.team_monthly_schedule')
    def test_get_nhl_team_monthly_schedule_success(self, mock_monthly_schedule):
        mock_monthly_schedule.return_value = [
            {"id": 1, "homeTeam": "BOS", "awayTeam": "TOR", "date": "2024-01-15"},
            {"id": 2, "homeTeam": "BOS", "awayTeam": "NJD", "date": "2024-01-20"}
        ]
        
        from nhl_api import get_nhl_team_monthly_schedule
        result = get_nhl_team_monthly_schedule("BOS", "2024-01")
        
        assert "games" in result
        assert result["team"] == "BOS"
        assert result["month"] == "2024-01"
        assert len(result["games"]) == 2
        
        mock_monthly_schedule.assert_called_once_with("BOS", "2024-01")
    
    @patch('nhl_api.client.schedule.team_monthly_schedule')
    def test_get_nhl_team_monthly_schedule_default_month(self, mock_monthly_schedule):
        mock_monthly_schedule.return_value = []
        
        from nhl_api import get_nhl_team_monthly_schedule
        result = get_nhl_team_monthly_schedule("BOS")
        
        assert "games" in result
        assert result["team"] == "BOS"
        assert result["month"] is None
        
        mock_monthly_schedule.assert_called_once_with("BOS", None)
    
    @patch('nhl_api.client.schedule.team_weekly_schedule')
    def test_get_nhl_team_weekly_schedule_success(self, mock_weekly_schedule):
        mock_weekly_schedule.return_value = [
            {"id": 1, "homeTeam": "BOS", "awayTeam": "TOR", "date": "2024-01-15"},
            {"id": 2, "homeTeam": "BOS", "awayTeam": "NJD", "date": "2024-01-17"}
        ]
        
        from nhl_api import get_nhl_team_weekly_schedule
        result = get_nhl_team_weekly_schedule("BOS", "2024-01-15")
        
        assert "games" in result
        assert result["team"] == "BOS"
        assert result["date"] == "2024-01-15"
        assert len(result["games"]) == 2
        
        mock_weekly_schedule.assert_called_once_with("BOS", "2024-01-15")
    
    @patch('nhl_api.client.schedule.team_season_schedule')
    def test_get_nhl_team_season_schedule_success(self, mock_season_schedule):
        mock_season_schedule.return_value = {
            "games": [
                {"id": 1, "homeTeam": "BOS", "awayTeam": "TOR", "date": "2024-01-15"},
                {"id": 2, "homeTeam": "BOS", "awayTeam": "NJD", "date": "2024-01-20"}
            ],
            "season": "20232024"
        }
        
        from nhl_api import get_nhl_team_season_schedule
        result = get_nhl_team_season_schedule("BOS", "20232024")
        
        assert "schedule" in result
        assert result["team"] == "BOS"
        assert result["season"] == "20232024"
        assert "games" in result["schedule"]
        
        mock_season_schedule.assert_called_once_with("BOS", "20232024")
    
    @patch('nhl_api.client.schedule.calendar_schedule')
    def test_get_nhl_calendar_schedule_success(self, mock_calendar_schedule):
        mock_calendar_schedule.return_value = {
            "date": "2024-01-15",
            "games": [
                {"id": 1, "homeTeam": "BOS", "awayTeam": "TOR", "startTime": "19:00"}
            ]
        }
        
        from nhl_api import get_nhl_calendar_schedule
        result = get_nhl_calendar_schedule("2024-01-15")
        
        assert "schedule" in result
        assert result["date"] == "2024-01-15"
        assert "games" in result["schedule"]
        
        mock_calendar_schedule.assert_called_once_with("2024-01-15")
    
    @patch('nhl_api.client.schedule.playoff_carousel')
    def test_get_nhl_playoff_carousel_success(self, mock_playoff_carousel):
        mock_playoff_carousel.return_value = {
            "series": [
                {"id": "a", "homeTeam": "BOS", "awayTeam": "TOR", "status": "active"},
                {"id": "b", "homeTeam": "NJD", "awayTeam": "NYR", "status": "active"}
            ]
        }
        
        from nhl_api import get_nhl_playoff_carousel
        result = get_nhl_playoff_carousel("20232024")
        
        assert "playoff_data" in result
        assert result["season"] == "20232024"
        assert "series" in result["playoff_data"]
        
        mock_playoff_carousel.assert_called_once_with("20232024")
    
    @patch('nhl_api.client.schedule.playoff_series_schedule')
    def test_get_nhl_playoff_series_schedule_success(self, mock_series_schedule):
        mock_series_schedule.return_value = {
            "series": "a",
            "games": [
                {"id": 1, "homeTeam": "BOS", "awayTeam": "TOR", "date": "2024-01-15"},
                {"id": 2, "homeTeam": "TOR", "awayTeam": "BOS", "date": "2024-01-17"}
            ]
        }
        
        from nhl_api import get_nhl_playoff_series_schedule
        result = get_nhl_playoff_series_schedule("20232024", "a")
        
        assert "series_schedule" in result
        assert result["season"] == "20232024"
        assert result["series"] == "a"
        assert "games" in result["series_schedule"]
        
        mock_series_schedule.assert_called_once_with("20232024", "a")
    
    @patch('nhl_api.client.schedule.playoff_bracket')
    def test_get_nhl_playoff_bracket_success(self, mock_playoff_bracket):
        mock_playoff_bracket.return_value = {
            "bracket": {
                "round1": [
                    {"series": "a", "homeTeam": "BOS", "awayTeam": "TOR"},
                    {"series": "b", "homeTeam": "NJD", "awayTeam": "NYR"}
                ]
            }
        }
        
        from nhl_api import get_nhl_playoff_bracket
        result = get_nhl_playoff_bracket("2024")
        
        assert "bracket" in result
        assert result["year"] == "2024"
        assert "round1" in result["bracket"]["bracket"]
        
        mock_playoff_bracket.assert_called_once_with("2024")
    
    def test_setup_nhl_tools_registers_all_tools(self):
        mock_mcp = Mock()
        
        setup_nhl_tools(mock_mcp)
        
        assert mock_mcp.tool.call_count == 17
        
        tool_calls = mock_mcp.tool.call_args_list
        assert len(tool_calls) == 17


if __name__ == "__main__":
    pytest.main([__file__])
