#!/usr/bin/env python3
"""
Calculate total statistics for each team across all years
"""

import csv
from collections import defaultdict

# Read the CSV file
with open('/Users/jwildfire/Desktop/fantasy_basketball_standings.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Dictionary to store team statistics
team_stats = defaultdict(lambda: {
    'seasons': 0,
    'wins': 0,
    'losses': 0,
    'ties': 0
})

# Calculate totals for each team
for row in data:
    team = row['Team']
    wins = int(row['Wins'])
    losses = int(row['Losses'])
    ties = int(row['Ties'])
    
    team_stats[team]['seasons'] += 1
    team_stats[team]['wins'] += wins
    team_stats[team]['losses'] += losses
    team_stats[team]['ties'] += ties

# Convert to list and sort by total wins (descending)
team_summary = []
for team, stats in team_stats.items():
    total_games = stats['wins'] + stats['losses'] + stats['ties']
    win_percentage = (stats['wins'] / total_games) if total_games > 0 else 0
    
    team_summary.append({
        'Team': team,
        'Seasons': stats['seasons'],
        'Wins': stats['wins'],
        'Losses': stats['losses'],
        'Ties': stats['ties'],
        'Total_Games': total_games,
        'Win_Percentage': round(win_percentage, 3)
    })

# Sort by total wins (descending)
team_summary.sort(key=lambda x: x['Wins'], reverse=True)

# Save to CSV
output_filename = '/Users/jwildfire/Desktop/team_career_stats.csv'
with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Team', 'Seasons', 'Wins', 'Losses', 'Ties', 'Total_Games', 'Win_Percentage']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in team_summary:
        writer.writerow(row)

# Display results
print("FANTASY BASKETBALL LEAGUE - CAREER STATISTICS")
print("=" * 80)
print(f"{'Team':<30} {'Seasons':<8} {'Wins':<6} {'Losses':<7} {'Ties':<5} {'Games':<6} {'Win%':<6}")
print("-" * 80)

for team in team_summary:
    print(f"{team['Team']:<30} {team['Seasons']:<8} {team['Wins']:<6} {team['Losses']:<7} {team['Ties']:<5} {team['Total_Games']:<6} {team['Win_Percentage']:<6.3f}")

print("\nTop 5 teams by total wins:")
for i, team in enumerate(team_summary[:5], 1):
    print(f"{i}. {team['Team']}: {team['Wins']} wins in {team['Seasons']} seasons")

print("\nTop 5 teams by win percentage (min 3 seasons):")
high_participation = [t for t in team_summary if t['Seasons'] >= 3]
high_participation.sort(key=lambda x: x['Win_Percentage'], reverse=True)
for i, team in enumerate(high_participation[:5], 1):
    print(f"{i}. {team['Team']}: {team['Win_Percentage']:.3f} ({team['Wins']}-{team['Losses']}-{team['Ties']} in {team['Seasons']} seasons)")

print(f"\nCareer statistics saved to: {output_filename}")