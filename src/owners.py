#!/usr/bin/env python3
"""
Add owner column to fantasy basketball CSV files
"""

import csv

owner_mapping = {
    'Utah Bootleggers': 'Trafton Drew',
    'The Penthouse Panda Bear': 'Jeremy Wildfire',
    'Austin Football Team': 'Ryan Mindell',
    'Toso Viti Toso': 'Ben Wildfire',
    "Im Trying Jennifer": 'Susheel Reddy',
    'Fly Nye Guy': 'Samuel Nye',
    'Miami Mambas': 'John Mapp',
    "Nowitzkis Fadeaway": 'Alex Tsung',
    'Bull City Bums': 'Nick Martin',
    'Baton Rouge Beasts': 'Tony Chen',
    'Austin CurryBrons': 'Ryan Mindell',  # Austin teams likely same owner
    'Mapp Stepback': 'John Mapp',        # Mapp in name
    "JMapps Stepover": 'John Mapp',      # Cleaned name
    'Team Carter': 'Matt Carter',
    'Team Davidai': 'Nadav Davidai',
    'Team Reddy': 'Susheel Reddy',       # Reddy in name
    'Team Nye': 'Samuel Nye',            # Nye in name
    'Ari 471': 'Ben Wildfire',           # Cleaned version of Ari 47/1
    'Ari 47/1': 'Ben Wildfire',
    'Lilongwe 327': 'Ben Wildfire',
    'UTEP 2 Steps': 'Jon Scheib',
    'Joe Biden Would Cross You Over': 'John Mapp',
    'Beto Would Cross You Over': 'John Mapp',
    'Mwambo Rd TIBA': 'Davide Ruscelli',
    'Bull City Bangers': 'Nick Martin',  # Bull City teams likely same owner
    'Uncanny Logo': 'Alex Tsung',
    'Teh Mehs': 'Jonathan Crisp',
    "Kawhis Laugh": 'Chris Carannante'
}

# Create simple owners mapping CSV
print("\nCreating owners mapping CSV...")
owners_csv_filename = '../data/owners.csv'
with open(owners_csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Team', 'Owner']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for team, owner in sorted(owner_mapping.items()):
        writer.writerow({'Team': team, 'Owner': owner})

print(f"Owners mapping saved to: {owners_csv_filename}")
