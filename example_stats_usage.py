#!/usr/bin/env python3
"""
Example script demonstrating the NHL Stats API functions.

This script shows how to use the various statistics endpoints
that have been added to the NHL API wrapper.
"""

from nhl_api import (
    get_nhl_gametypes_per_season_by_team,
    get_nhl_player_career_stats,
    get_nhl_player_game_log,
    get_nhl_team_summary_stats,
    get_nhl_skater_stats_summary,
    get_nhl_goalie_stats_summary
)

def main():
    print("NHL Stats API Examples")
    print("=" * 50)
    
    # Example 1: Get game types per season for Toronto Maple Leafs
    print("\n1. Game Types per Season for Toronto Maple Leafs:")
    print("-" * 45)
    result = get_nhl_gametypes_per_season_by_team("TOR")
    if "gametypes" in result:
        gametypes = result["gametypes"]
        print(f"Found {len(gametypes)} seasons")
        for season_data in gametypes[:3]:  # Show first 3 seasons
            season = season_data.get("season", "Unknown")
            game_types = season_data.get("gameTypes", [])
            game_type_names = []
            for gt in game_types:
                if gt == 1:
                    game_type_names.append("Preseason")
                elif gt == 2:
                    game_type_names.append("Regular Season")
                elif gt == 3:
                    game_type_names.append("Playoffs")
                else:
                    game_type_names.append(f"Unknown ({gt})")
            print(f"  Season {season}: {', '.join(game_type_names)}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    # Example 2: Get Connor McDavid's career stats
    print("\n2. Connor McDavid Career Stats:")
    print("-" * 35)
    result = get_nhl_player_career_stats("8478402")
    if "player_stats" in result:
        stats = result["player_stats"]
        print(f"Name: {stats.get('firstName', {}).get('default', 'N/A')} {stats.get('lastName', {}).get('default', 'N/A')}")
        print(f"Position: {stats.get('position', 'N/A')}")
        print(f"Team: {stats.get('currentTeamAbbrev', 'N/A')}")
        print(f"Active: {stats.get('isActive', 'N/A')}")
        print(f"Jersey Number: {stats.get('sweaterNumber', 'N/A')}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    # Example 3: Get team summary stats for Florida Panthers (2021-2022 season)
    print("\n3. Team Summary Stats - Florida Panthers (2021-2022):")
    print("-" * 55)
    result = get_nhl_team_summary_stats("20202021", "20212022", 2)
    if "team_summary" in result:
        teams = result["team_summary"]
        # Find Florida Panthers
        panthers = next((team for team in teams if "Panthers" in team.get("teamFullName", "")), None)
        if panthers:
            print(f"Team: {panthers.get('teamFullName', 'N/A')}")
            print(f"Season: {panthers.get('seasonId', 'N/A')}")
            print(f"Games Played: {panthers.get('gamesPlayed', 'N/A')}")
            print(f"Wins: {panthers.get('wins', 'N/A')}")
            print(f"Losses: {panthers.get('losses', 'N/A')}")
            print(f"Points: {panthers.get('points', 'N/A')}")
            print(f"Goals For: {panthers.get('goalsFor', 'N/A')}")
            print(f"Goals Against: {panthers.get('goalsAgainst', 'N/A')}")
        else:
            print("Florida Panthers not found in results")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    # Example 4: Get top skater stats for 2023-2024 season
    print("\n4. Top Skater Stats (2023-2024 Season):")
    print("-" * 40)
    result = get_nhl_skater_stats_summary("20232024", "20232024", limit=5)
    if "skater_stats" in result:
        skaters = result["skater_stats"]
        print(f"Top {len(skaters)} skaters by points:")
        for i, skater in enumerate(skaters, 1):
            name = skater.get("skaterFullName", "Unknown")
            points = skater.get("points", 0)
            goals = skater.get("goals", 0)
            assists = skater.get("assists", 0)
            games = skater.get("gamesPlayed", 0)
            print(f"  {i}. {name}: {points} pts ({goals}G, {assists}A) in {games} games")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    # Example 5: Get top goalie stats for 2024-2025 season
    print("\n5. Top Goalie Stats (2024-2025 Season):")
    print("-" * 40)
    result = get_nhl_goalie_stats_summary("20242025", "20242025", "summary", limit=5)
    if "goalie_stats" in result:
        goalies = result["goalie_stats"]
        print(f"Top {len(goalies)} goalies by wins:")
        for i, goalie in enumerate(goalies, 1):
            name = goalie.get("goalieFullName", "Unknown")
            wins = goalie.get("wins", 0)
            losses = goalie.get("losses", 0)
            gaa = goalie.get("goalsAgainstAverage", 0)
            save_pct = goalie.get("savePct", 0)
            shutouts = goalie.get("shutouts", 0)
            print(f"  {i}. {name}: {wins}W-{losses}L, {gaa:.2f} GAA, {save_pct:.3f} SV%, {shutouts} SO")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    # Example 6: Get player game log (Connor McDavid, 2024-2025 season, regular season)
    print("\n6. Connor McDavid Game Log (2024-2025 Regular Season):")
    print("-" * 55)
    result = get_nhl_player_game_log("8478402", "20242025", 2)
    if "game_log" in result:
        games = result["game_log"]
        if games:
            print(f"Found {len(games)} games")
            # Show last 3 games
            recent_games = games[-3:] if len(games) >= 3 else games
            for game in recent_games:
                date = game.get("gameDate", "Unknown")
                goals = game.get("goals", 0)
                assists = game.get("assists", 0)
                points = game.get("points", 0)
                plus_minus = game.get("plusMinus", 0)
                shots = game.get("shots", 0)
                toi = game.get("toi", "Unknown")
                print(f"  {date}: {goals}G {assists}A {points}P, +/-{plus_minus}, {shots} shots, {toi} TOI")
        else:
            print("No games found")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
