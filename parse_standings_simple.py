#!/usr/bin/env python3
"""
Parse fantasy basketball league standings from HTML and create CSV using only built-in libraries
"""

import re
import csv
import html

# Read the HTML file
with open('/Users/jwildfire/Desktop/gm_standings.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Store all data
all_standings = []

# Find all year sections using regex
year_pattern = r'<span class="jsx-1093571074 year-text">(\d{4})</span>'
years = re.findall(year_pattern, html_content)

# Split content by year sections
year_sections = re.split(r'<span class="jsx-1093571074 year-text">\d{4}</span>', html_content)

for i, year in enumerate(years):
    if i + 1 >= len(year_sections):
        continue
        
    section_content = year_sections[i + 1]
    print(f"Processing year: {year}")
    
    # Find table rows with team data
    # Look for patterns like: title="Team Name"...>Team Name</span>...11-8-0
    team_pattern = r'title="([^"]+)"[^>]*class="teamName[^"]*"[^>]*>([^<]+)</span>.*?<span[^>]*>(\d+-\d+-\d+)</span>'
    
    matches = re.findall(team_pattern, section_content, re.DOTALL)
    
    for match in matches:
        team_name = html.unescape(match[0].strip())
        record_text = match[2].strip()
        
        # Parse record using regex to handle format like "11-8-0"
        record_match = re.match(r'(\d+)-(\d+)-(\d+)', record_text)
        if record_match:
            wins = int(record_match.group(1))
            losses = int(record_match.group(2))
            ties = int(record_match.group(3))
            
            all_standings.append({
                'Year': year,
                'Team': team_name,
                'Wins': wins,
                'Losses': losses,
                'Ties': ties
            })

# Sort by year and team name for consistency
all_standings.sort(key=lambda x: (x['Year'], x['Team']))

# Write to CSV
csv_filename = '/Users/jwildfire/Desktop/fantasy_basketball_standings.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Year', 'Team', 'Wins', 'Losses', 'Ties']
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
    print(f"{row['Year']}: {row['Team']} - {row['Wins']}-{row['Losses']}-{row['Ties']}")