#!/usr/bin/env python3
"""
Merge rawStandings.csv with owners.csv to create ownersStandings.csv
"""

import csv

# Read owners mapping
print("Reading owners mapping...")
owners_map = {}
with open('../data/owners.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        owners_map[row['Team']] = row['Owner']

print(f"Loaded {len(owners_map)} team-owner mappings")

# Read raw standings and merge with owners
print("Reading raw standings and merging with owners...")
merged_data = []
with open('../data/rawStandings.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        team = row['Team']
        owner = owners_map.get(team, 'Unknown')
        
        # Create merged record
        merged_record = {
            'Year': row['Year'],
            'Team': team,
            'Owner': owner,
            'Rank': row['Rank'],
            'Wins': row['Wins'],
            'Losses': row['Losses'],
            'Ties': row['Ties']
        }
        merged_data.append(merged_record)

print(f"Merged {len(merged_data)} records")

# Write merged data to CSV
output_filename = '../data/ownersStandings.csv'
with open(output_filename, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Year', 'Team', 'Owner', 'Rank', 'Wins', 'Losses', 'Ties']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    writer.writeheader()
    for record in merged_data:
        writer.writerow(record)

print(f"Merged standings saved to: {output_filename}")

# Create aggregated data across all seasons
print("\nCreating overall aggregated standings...")
owner_totals = {}
for record in merged_data:
    owner = record['Owner']
    if owner not in owner_totals:
        owner_totals[owner] = {
            'Owner': owner,
            'Total_Wins': 0,
            'Total_Losses': 0,
            'Total_Ties': 0,
            'Seasons_Played': 0,
            'Rank_Total': 0,
            'Championships': 0,
            'Finals': 0,
            'Playoffs': 0
        }
    
    owner_totals[owner]['Total_Wins'] += int(record['Wins'])
    owner_totals[owner]['Total_Losses'] += int(record['Losses'])
    owner_totals[owner]['Total_Ties'] += int(record['Ties'])
    owner_totals[owner]['Seasons_Played'] += 1
    
    # Track rank statistics
    rank = int(record['Rank'])
    owner_totals[owner]['Rank_Total'] += rank
    
    # Count achievements based on final rank
    if rank == 1:
        owner_totals[owner]['Championships'] += 1
    if rank <= 2:
        owner_totals[owner]['Finals'] += 1
    if rank <= 4:
        owner_totals[owner]['Playoffs'] += 1

# Calculate additional stats
for owner_data in owner_totals.values():
    total_games = owner_data['Total_Wins'] + owner_data['Total_Losses'] + owner_data['Total_Ties']
    owner_data['Total_Games'] = total_games
    if total_games > 0:
        owner_data['Win_Percentage'] = round(owner_data['Total_Wins'] / total_games, 3)
    else:
        owner_data['Win_Percentage'] = 0.0
    
    # Calculate rank statistics
    if owner_data['Seasons_Played'] > 0:
        owner_data['Average_Rank'] = round(owner_data['Rank_Total'] / owner_data['Seasons_Played'], 1)
    else:
        owner_data['Average_Rank'] = 0.0

# Sort by win percentage (descending)
aggregated_data = sorted(owner_totals.values(), key=lambda x: x['Win_Percentage'], reverse=True)

# Write aggregated data to CSV
overall_filename = '../data/ownersStandingsOverall.csv'
with open(overall_filename, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Owner', 'Seasons_Played', 'Total_Games', 'Total_Wins', 'Total_Losses', 'Total_Ties', 'Win_Percentage', 'Average_Rank', 'Championships', 'Finals', 'Playoffs']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    writer.writeheader()
    for record in aggregated_data:
        # Remove internal tracking fields before writing
        output_record = {k: v for k, v in record.items() if k in fieldnames}
        writer.writerow(output_record)

print(f"Overall standings saved to: {overall_filename}")

# Show summary statistics
years = sorted(set(record['Year'] for record in merged_data))
owners = sorted(set(record['Owner'] for record in merged_data))
teams = sorted(set(record['Team'] for record in merged_data))

print(f"\nSummary:")
print(f"Years: {len(years)} ({years[0]} - {years[-1]})")
print(f"Teams: {len(teams)}")
print(f"Owners: {len(owners)}")
print(f"Total records: {len(merged_data)}")

# Show owner distribution
owner_counts = {}
for record in merged_data:
    owner = record['Owner']
    owner_counts[owner] = owner_counts.get(owner, 0) + 1

print(f"\nRecords per owner:")
for owner, count in sorted(owner_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {owner}: {count} records")

print(f"\nSample merged data:")
for i, record in enumerate(merged_data[:5]):
    print(f"  {record['Year']}: #{record['Rank']} {record['Team']} ({record['Owner']}) - {record['Wins']}-{record['Losses']}-{record['Ties']}")

print(f"\nOverall standings (by win percentage):")
for i, record in enumerate(aggregated_data[:10]):  # Show top 10
    print(f"  {i+1}. {record['Owner']}: {record['Total_Wins']}-{record['Total_Losses']}-{record['Total_Ties']} ({record['Win_Percentage']:.3f}) in {record['Seasons_Played']} seasons")