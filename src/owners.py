#!/usr/bin/env python3
"""
Add owner column to fantasy basketball CSV files
"""

import csv

owner_mapping = {
    'Utah Bootleggers': 'Trafton',
    'The Penthouse Panda Bear': 'Jeremy',
    'Austin Football Team': 'Ryan',
    'Toso Viti Toso': 'Ben',
    "Im Trying Jennifer": 'Susheel',
    'Fly Nye Guy': 'Samuel',
    'Miami Mambas': 'John',
    "Nowitzkis Fadeaway": 'Alex',
    'Bull City Bums': 'Nick',
    'Baton Rouge Beasts': 'Tony',
    'Austin CurryBrons': 'Ryan',  # Austin teams likely same owner
    'Mapp Stepback': 'John',        # Mapp in name
    "JMapps Stepover": 'John',      # Cleaned name
    'Team Carter': 'Matt',
    'Team Davidai': 'Nadav',
    'Team Reddy': 'Susheel',       # Reddy in name
    'Team Nye': 'Samuel',            # Nye in name
    'Ari 471': 'Ben',           # Cleaned version of Ari 47/1
    'Ari 47/1': 'Ben',
    'Lilongwe 327': 'Ben',
    'UTEP 2 Steps': 'Jon',
    'Joe Biden Would Cross You Over': 'John',
    'Beto Would Cross You Over': 'John',
    'Mwambo Rd TIBA': 'Davide',
    'Bull City Bangers': 'Nick',  # Bull City teams likely same owner
    'Uncanny Logo': 'Alex',
    'Teh Mehs': 'Jonathan',
    "Kawhis Laugh": 'Chris'
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
