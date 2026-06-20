#!/usr/bin/env python3
"""
2026 World Cup Arena - Data Collection Script
This script collects and updates team data from various sources.
Run this script to refresh the data in src/data/teams.json
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

DATA_FILE = project_root / "src" / "data" / "teams.json"

def load_teams():
    """Load existing team data"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_teams(teams):
    """Save team data to JSON file"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(teams, f, ensure_ascii=False, indent=2)
    print(f"Data saved to {DATA_FILE}")

def calculate_team_ratings(team):
    """
    Calculate team ratings based on various factors.
    This is a simplified model - you can enhance it with real data.
    """
    # Base ratings from FIFA ranking (inverse - lower rank = higher rating)
    fifa_rank = team.get('fifaRanking', 50)
    base_rating = max(60, 100 - fifa_rank)
    
    # Adjust based on historical performance
    history = team.get('worldCupHistory', [])
    titles = sum(1 for h in history if '冠军' in h.get('result', '') or 'Champion' in h.get('resultEn', ''))
    finals = sum(1 for h in history if '亚军' in h.get('result', '') or 'Runner-up' in h.get('resultEn', ''))
    
    experience_bonus = titles * 3 + finals * 2
    
    # Generate ratings with some randomness based on team profile
    ratings = {
        'attack': min(95, base_rating + experience_bonus + 5),
        'defense': min(95, base_rating + experience_bonus),
        'midfield': min(95, base_rating + experience_bonus + 2),
        'physical': min(95, base_rating + 3),
        'tactics': min(95, base_rating + experience_bonus + 4),
        'experience': min(95, base_rating + experience_bonus * 2),
    }
    
    return ratings

def update_ratings():
    """Update all team ratings"""
    teams = load_teams()
    
    for team in teams:
        team['ratings'] = calculate_team_ratings(team)
        print(f"Updated {team['name']}: ratings = {team['ratings']}")
    
    save_teams(teams)
    print(f"\nUpdated ratings for {len(teams)} teams")

def add_team(team_data):
    """Add a new team to the dataset"""
    teams = load_teams()
    
    # Check if team already exists
    existing = [t for t in teams if t['id'] == team_data['id']]
    if existing:
        print(f"Team {team_data['id']} already exists. Use update_team() instead.")
        return
    
    # Calculate ratings if not provided
    if 'ratings' not in team_data:
        team_data['ratings'] = calculate_team_ratings(team_data)
    
    teams.append(team_data)
    save_teams(teams)
    print(f"Added team: {team_data['name']}")

def update_team(team_id, updates):
    """Update specific fields of a team"""
    teams = load_teams()
    
    for team in teams:
        if team['id'] == team_id:
            team.update(updates)
            save_teams(teams)
            print(f"Updated team: {team['name']}")
            return
    
    print(f"Team {team_id} not found")

def generate_report():
    """Generate a summary report of all teams"""
    teams = load_teams()
    
    print("=" * 60)
    print("2026 World Cup Arena - Team Data Report")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    print(f"\nTotal Teams: {len(teams)}")
    
    # By confederation
    confs = {}
    for t in teams:
        confs[t['confederation']] = confs.get(t['confederation'], 0) + 1
    print("\nBy Confederation:")
    for conf, count in sorted(confs.items()):
        print(f"  {conf}: {count}")
    
    # By group
    groups = {}
    for t in teams:
        groups[t['group']] = groups.get(t['group'], 0) + 1
    print("\nBy Group:")
    for group, count in sorted(groups.items()):
        print(f"  Group {group}: {count}")
    
    # Top 10 by FIFA ranking
    print("\nTop 10 by FIFA Ranking:")
    for t in sorted(teams, key=lambda x: x['fifaRanking'])[:10]:
        avg_rating = sum(t['ratings'].values()) / 6
        print(f"  #{t['fifaRanking']:2d} {t['name']:15s} - Avg Rating: {avg_rating:.1f}")
    
    # Top 10 by average rating
    print("\nTop 10 by Average Rating:")
    sorted_by_rating = sorted(teams, key=lambda x: sum(x['ratings'].values()) / 6, reverse=True)
    for t in sorted_by_rating[:10]:
        avg_rating = sum(t['ratings'].values()) / 6
        print(f"  {avg_rating:.1f} {t['name']:15s} - FIFA #{t['fifaRanking']}")
    
    print("\n" + "=" * 60)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='World Cup Arena Data Manager')
    parser.add_argument('command', choices=['update-ratings', 'report', 'validate'],
                       help='Command to execute')
    
    args = parser.parse_args()
    
    if args.command == 'update-ratings':
        update_ratings()
    elif args.command == 'report':
        generate_report()
    elif args.command == 'validate':
        teams = load_teams()
        print(f"Validating {len(teams)} teams...")
        errors = []
        for team in teams:
            required = ['id', 'name', 'nameEn', 'fifaCode', 'flag', 'fifaRanking', 
                       'confederation', 'group', 'coach', 'players', 'recentResults', 
                       'ratings', 'worldCupHistory']
            for field in required:
                if field not in team:
                    errors.append(f"{team.get('id', 'UNKNOWN')}: missing {field}")
        
        if errors:
            print(f"Found {len(errors)} errors:")
            for e in errors:
                print(f"  - {e}")
        else:
            print("All teams validated successfully!")

if __name__ == '__main__':
    main()
