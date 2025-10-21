#!/usr/bin/env python3
"""
Parse fantasy basketball league standings from HTML and create raw CSV
"""

import re
import csv
from bs4 import BeautifulSoup

def clean_team_name(name):
    """Keep only alphanumeric characters and spaces in team names"""
    # Use regex to keep only letters, numbers, and spaces
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', name)
    # Replace multiple spaces with single space and strip
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

# Read the HTML file
with open('../raw/gm_standings.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Parse HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find all year sections
year_sections = soup.find_all('div', class_='season-container')

# Store all data
all_standings = []

for section in year_sections:
    # Extract year
    year_header = section.find('span', class_='year-text')
    if not year_header:
        continue
    
    year = year_header.text.strip()
    print(f"Processing year: {year}")
    
    # Find the standings table in this section
    table = section.find('table', class_='Table')
    if not table:
        continue
        
    # Find all team rows
    rows = table.find('tbody').find_all('tr')
    
    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 3:
            continue
            
        # Extract rank from first cell
        rank_cell = cells[0]
        rank_text = rank_cell.get_text().strip()
        try:
            rank = int(rank_text)
        except (ValueError, TypeError):
            continue  # Skip if rank is not a valid number
            
        # Extract team name
        team_cell = cells[1]
        team_span = team_cell.find('span', {'title': True})
        if not team_span:
            continue
            
        team_name = team_span.get('title').strip()
        
        # Clean special characters from team name
        team_name = clean_team_name(team_name)
        
        # Extract record (wins-losses-ties format)
        record_cell = cells[2]
        record_text = record_cell.get_text().strip()
        
        # Parse record using regex to handle format like "11-8-0"
        record_match = re.match(r'(\d+)-(\d+)-(\d+)', record_text)
        if record_match:
            wins = int(record_match.group(1))
            losses = int(record_match.group(2))
            ties = int(record_match.group(3))
            
            all_standings.append({
                'Year': year,
                'Team': team_name,
                'Rank': rank,
                'Wins': wins,
                'Losses': losses,
                'Ties': ties
            })

# Sort by year and team name for consistency
all_standings.sort(key=lambda x: (x['Year'], x['Team']))

# Write to CSV
csv_filename = '../data/fbStandings.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Year', 'Team', 'Rank', 'Wins', 'Losses', 'Ties']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in all_standings:
        writer.writerow(row)

print(f"\nData extraction complete!")
print(f"Total records: {len(all_standings)}")
print(f"Years covered: {sorted(set(row['Year'] for row in all_standings))}")
print(f"CSV file saved as: {csv_filename}")

# Display a sample of the data
print("\nSample data:")
for i, row in enumerate(all_standings[:10]):
    print(f"{row['Year']}: #{row['Rank']} {row['Team']} - {row['Wins']}-{row['Losses']}-{row['Ties']}")