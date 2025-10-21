# Fantasy Basketball League Data Analysis

A comprehensive analysis of ESPN fantasy basketball league standings from 2017-2025.

## Project Structure

```
grudgematch/
├── README.md
├── league_analysis_report.html          # Interactive HTML report with sortable tables
├── raw/
│   └── gm_standings.html                # Original ESPN league standings HTML data
├── data/
│   ├── rawStandings.csv                 # Raw standings data from BeautifulSoup parser (96 records)
│   ├── ownersStandings.csv              # Merged standings with owner information (96 records)
│   ├── fantasy_basketball_standings.csv # Year-by-year team standings data (96 records)
│   ├── team_career_stats.csv           # Career totals and win percentages for all teams (27 teams)
│   ├── owner_career_stats.csv          # Career statistics aggregated by owner (16 owners)
│   └── owners.csv                       # Simple team-to-owner mapping (27 teams)
└── src/
    ├── rawStandings.py                  # Alternative HTML parser (uses BeautifulSoup)
    ├── parse_standings_simple.py       # Extract data from HTML (regex-based)
    ├── ownersStandings.py               # Merge rawStandings with owners
    ├── calculate_team_stats.py         # Calculate career statistics
    ├── add_owners.py                   # Add owner information to CSV files
    └── analyze_owners.py               # Generate owner-based statistics
```

## Data Structure

### rawStandings.csv
- **Year**: Season year (2017-2025)
- **Team**: Team name
- **Wins**: Regular season wins
- **Losses**: Regular season losses
- **Ties**: Regular season ties

### ownersStandings.csv
- **Year**: Season year (2017-2025)
- **Team**: Team name
- **Owner**: Team owner name
- **Wins**: Regular season wins
- **Losses**: Regular season losses
- **Ties**: Regular season ties

### fantasy_basketball_standings.csv
- **Year**: Season year (2017-2025) 
- **Team**: Team name
- **Owner**: Team owner name (added from 2025 season data)
- **Wins**: Regular season wins
- **Losses**: Regular season losses  
- **Ties**: Regular season ties

### team_career_stats.csv
- **Team**: Team name
- **Owner**: Team owner name
- **Seasons**: Number of seasons played
- **Wins**: Total career wins
- **Losses**: Total career losses
- **Ties**: Total career ties
- **Win_Percentage**: Career win percentage

### owner_career_stats.csv
- **Owner**: Owner name
- **Teams**: Number of teams owned
- **Team_Names**: List of team names owned
- **Total_Seasons**: Total seasons across all teams
- **Total_Wins**: Total wins across all teams
- **Total_Losses**: Total losses across all teams
- **Total_Ties**: Total ties across all teams
- **Total_Games**: Total games played
- **Win_Percentage**: Overall win percentage

### owners.csv
- **Team**: Team name
- **Owner**: Owner name (simple mapping table)

## Usage

### Option 1: Using the regex-based parser (recommended)
```bash
cd src
python3 parse_standings_simple.py
python3 calculate_team_stats.py
python3 add_owners.py
python3 analyze_owners.py
```

### Option 2: Using the BeautifulSoup parser
```bash
cd src
python3 rawStandings.py              # Creates rawStandings.csv
python3 ownersStandings.py           # Merges rawStandings.csv + owners.csv → ownersStandings.csv
python3 calculate_team_stats.py
python3 add_owners.py
python3 analyze_owners.py
```

### Option 3: Simple merge workflow
```bash
cd src
python3 rawStandings.py              # Parse HTML → rawStandings.csv
python3 add_owners.py                # Create owners.csv mapping
python3 ownersStandings.py           # Merge → ownersStandings.csv (ready for analysis)
```

Or run the complete analysis pipeline:
```bash
cd src
python3 parse_standings_simple.py && python3 calculate_team_stats.py && python3 add_owners.py && python3 analyze_owners.py
```

**Note**: The scripts will:
- Read raw data from `../raw/gm_standings.html`
- Output processed CSV files to `../data/`
- Create the interactive HTML report in the root directory

## League Statistics

- **Total Teams**: 27 unique teams across 9 seasons
- **Total Records**: 96 team-season records
- **Season Format**: ~19-20 games per team per season
- **Known Owners**: 10 owners identified for 16 teams (11 teams marked "Unknown")

## Top Performers

### By Total Wins
1. Jeremy Wildfire: 107 wins (The Penthouse Panda Bear)
2. Ryan Mindell: 106 wins (Austin Football Team, Austin CurryBrons)
3. Tony Chen: 76 wins (Baton Rouge Beasts)

### By Win Percentage (minimum 50 games)
1. Jeremy Wildfire: 62.6% (107-63-1)
2. Ben Wildfire: 62.2% (23-14-0) 
3. Ryan Mindell: 62.0% (106-63-2)