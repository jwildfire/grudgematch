# Fantasy Basketball League Analysis - Grudgematch

This directory contains the complete analysis of fantasy basketball league standings data from 2017-2025.

## Files

### Data Files
- `gm_standings.html` - Original HTML file containing league standings from ESPN
- `fantasy_basketball_standings.csv` - Parsed standings data with one row per team per year
- `team_career_stats.csv` - Career statistics summary for each team across all years

### Scripts
- `parse_standings.py` - Initial parsing script (requires BeautifulSoup)
- `parse_standings_simple.py` - Working parser using only built-in Python libraries
- `calculate_team_stats.py` - Script to generate career statistics for each team

## Data Summary

### League Overview
- **Years covered:** 2017-2025 (9 seasons)
- **Total records:** 96 team-seasons
- **Unique teams:** 27 different teams
- **League size:** 10-12 teams per year

### Top Performers

#### Most Total Wins
1. The Penthouse Panda Bear - 107 wins in 9 seasons (.626 win%)
2. Team Carter - 77 wins in 7 seasons (.575 win%)
3. Baton Rouge Beasts - 76 wins in 9 seasons (.444 win%)
4. Utah Bootleggers - 74 wins in 9 seasons (.433 win%)
5. I'm Trying Jennifer - 71 wins in 7 seasons (.538 win%)

#### Best Win Percentages (minimum 3 seasons)
1. Austin CurryBrons - .644 (38-21-0 in 3 seasons)
2. The Penthouse Panda Bear - .626 (107-63-1 in 9 seasons)
3. Austin Football Team - .607 (68-42-2 in 6 seasons)
4. Team Carter - .575 (77-56-1 in 7 seasons)
5. I'm Trying Jennifer - .538 (71-60-1 in 7 seasons)

## Usage

To regenerate the analysis:

1. **Parse HTML standings:**
   ```bash
   python3 parse_standings_simple.py
   ```

2. **Calculate career statistics:**
   ```bash
   python3 calculate_team_stats.py
   ```

## Data Format

### fantasy_basketball_standings.csv
- `Year` - Season year
- `Team` - Team name
- `Wins` - Regular season wins
- `Losses` - Regular season losses
- `Ties` - Regular season ties

### team_career_stats.csv
- `Team` - Team name
- `Seasons` - Number of seasons played
- `Wins` - Total career wins
- `Losses` - Total career losses
- `Ties` - Total career ties
- `Total_Games` - Total games played
- `Win_Percentage` - Career win percentage