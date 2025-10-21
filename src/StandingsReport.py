#!/usr/bin/env python3
"""
Generate HTML Summary Report for Fantasy Basketball League Overall Standings

This script reads the ownersStandingsOverall.csv file and creates a comprehensive
HTML report showing career statistics for all owners.
"""

import csv
import datetime
import json
from pathlib import Path

def read_overall_standings():
    """Read the overall standings CSV file"""
    standings = []
    csv_path = Path(__file__).parent / '../data/ownersStandingsOverall.csv'
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric fields
            row['Seasons_Played'] = int(row['Seasons_Played'])
            row['Total_Games'] = int(row['Total_Games'])
            row['Total_Wins'] = int(row['Total_Wins'])
            row['Total_Losses'] = int(row['Total_Losses'])
            row['Total_Ties'] = int(row['Total_Ties'])
            row['Win_Percentage'] = float(row['Win_Percentage'])
            standings.append(row)
    
    return standings

def read_detailed_standings():
    """Read the detailed standings CSV file for chart data"""
    standings = []
    csv_path = Path(__file__).parent / '../data/ownersStandings.csv'
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric fields
            row['Year'] = int(row['Year'])
            row['Wins'] = int(row['Wins'])
            row['Losses'] = int(row['Losses'])
            row['Ties'] = int(row['Ties'])
            standings.append(row)
    
    return standings

def prepare_chart_data(detailed_standings):
    """Prepare data for the wins vs year chart"""
    # Group data by owner
    owners_data = {}
    all_years = set()
    
    for record in detailed_standings:
        owner = record['Owner']
        year = record['Year']
        wins = record['Wins']
        
        all_years.add(year)
        
        if owner not in owners_data:
            owners_data[owner] = {}
        
        owners_data[owner][year] = wins
    
    # Sort years
    sorted_years = sorted(all_years)
    
    # Create chart datasets
    chart_data = {
        'labels': sorted_years,
        'datasets': []
    }
    
    # Color palette for lines
    colors = [
        '#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6',
        '#1abc9c', '#34495e', '#e67e22', '#95a5a6', '#f1c40f',
        '#16a085', '#2980b9', '#8e44ad', '#27ae60', '#d35400',
        '#7f8c8d'
    ]
    
    color_index = 0
    for owner, year_wins in owners_data.items():
        # Create data points for this owner
        data_points = []
        seasons_played = 0
        
        for year in sorted_years:
            wins = year_wins.get(year, None)  # None if owner didn't play that year
            if wins is not None:
                seasons_played += 1
            data_points.append(wins)
        
        # Only show by default if owner has 5+ seasons
        is_visible = seasons_played >= 5
        
        chart_data['datasets'].append({
            'label': owner,
            'data': data_points,
            'borderColor': colors[color_index % len(colors)],
            'backgroundColor': colors[color_index % len(colors)] + '20',  # 20% opacity
            'tension': 0.1,
            'spanGaps': True,  # Connect points even if there are null values
            'hidden': not is_visible  # Hide owners with < 5 seasons by default
        })
        
        color_index += 1
    
    return chart_data

def calculate_additional_stats(standings):
    """Calculate additional statistics for the report"""
    total_seasons = sum(owner['Seasons_Played'] for owner in standings)
    total_games = sum(owner['Total_Games'] for owner in standings)
    total_owners = len(standings)
    
    # Find best/worst records
    best_win_pct = max(standings, key=lambda x: x['Win_Percentage'])
    worst_win_pct = min(standings, key=lambda x: x['Win_Percentage'])
    most_wins = max(standings, key=lambda x: x['Total_Wins'])
    most_losses = max(standings, key=lambda x: x['Total_Losses'])
    most_seasons = max(standings, key=lambda x: x['Seasons_Played'])
    
    return {
        'total_seasons': total_seasons,
        'total_games': total_games,
        'total_owners': total_owners,
        'best_win_pct': best_win_pct,
        'worst_win_pct': worst_win_pct,
        'most_wins': most_wins,
        'most_losses': most_losses,
        'most_seasons': most_seasons
    }

def get_win_pct_class(win_pct):
    """Return CSS class based on win percentage"""
    if win_pct >= 0.600:
        return 'excellent'
    elif win_pct >= 0.550:
        return 'good'
    elif win_pct >= 0.500:
        return 'average'
    elif win_pct >= 0.450:
        return 'below-average'
    else:
        return 'poor'

def generate_html_report(standings, stats, chart_data):
    """Generate the HTML report"""
    
    # Get current timestamp
    timestamp = datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fantasy Basketball League - Overall Standings Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        
        h2 {{
            color: #34495e;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 5px;
            margin-top: 30px;
        }}
        
        .timestamp {{
            text-align: center;
            color: #7f8c8d;
            font-style: italic;
            margin-bottom: 30px;
        }}
        
        .summary-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #3498db;
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .stat-label {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background-color: white;
        }}
        
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        
        th {{
            background-color: #34495e;
            color: white;
            font-weight: bold;
            position: sticky;
            top: 0;
        }}
        
        th:not(:first-child) {{
            transition: background-color 0.2s ease;
        }}
        
        th:not(:first-child):hover {{
            background-color: #2c3e50;
        }}
        
        th.sort-asc, th.sort-desc {{
            background-color: #2980b9;
        }}
        
        th.sort-asc:hover, th.sort-desc:hover {{
            background-color: #3498db;
        }}
        
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        tr:hover {{
            background-color: #e8f4f8;
        }}
        
        .rank {{
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .owner-name {{
            font-weight: bold;
            color: #2980b9;
        }}
        
        .win-pct {{
            font-weight: bold;
            border-radius: 4px;
            padding: 4px 8px;
        }}
        
        .excellent {{ background-color: #2ecc71; color: white; }}
        .good {{ background-color: #f39c12; color: white; }}
        .average {{ background-color: #95a5a6; color: white; }}
        .below-average {{ background-color: #e67e22; color: white; }}
        .poor {{ background-color: #e74c3c; color: white; }}
        
        .record {{
            font-family: 'Courier New', monospace;
            background-color: #ecf0f1;
            padding: 2px 6px;
            border-radius: 3px;
        }}
        
        .highlights {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .highlight-card {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #e74c3c;
        }}
        
        .highlight-title {{
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        
        .highlight-value {{
            font-size: 1.2em;
            color: #e74c3c;
        }}
        
        .legend {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        
        .legend-title {{
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
        }}
        
        .legend-items {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 3px;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 15px;
            }}
            
            table {{
                font-size: 0.9em;
            }}
            
            .summary-stats {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container">
        <h1>🏀 Fantasy Basketball League<br>Overall Standings Report</h1>
        <div class="timestamp">Generated on {timestamp}</div>
        
        <h2>📊 League Summary</h2>
        <div class="summary-stats">
            <div class="stat-card">
                <div class="stat-number">{stats['total_owners']}</div>
                <div class="stat-label">Total Owners</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['total_seasons']}</div>
                <div class="stat-label">Total Seasons Played</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['total_games']:,}</div>
                <div class="stat-label">Total Games Played</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len([o for o in standings if o['Seasons_Played'] >= 5])}</div>
                <div class="stat-label">Veteran Owners (5+ seasons)</div>
            </div>
        </div>
        
        <div class="legend">
            <div class="legend-title">Win Percentage Legend:</div>
            <div class="legend-items">
                <div class="legend-item">
                    <div class="legend-color excellent"></div>
                    <span>Excellent (60%+)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color good"></div>
                    <span>Good (55-59%)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color average"></div>
                    <span>Average (50-54%)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color below-average"></div>
                    <span>Below Average (45-49%)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color poor"></div>
                    <span>Poor (&lt;45%)</span>
                </div>
            </div>
        </div>
        
        <h2>🏆 Career Standings</h2>
        <table>
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Owner</th>
                    <th>Seasons</th>
                    <th>Record</th>
                    <th>Win %</th>
                    <th>Total Games</th>
                    <th>Avg Games/Season</th>
                </tr>
            </thead>
            <tbody>"""
    
    for i, owner in enumerate(standings, 1):
        win_pct_class = get_win_pct_class(owner['Win_Percentage'])
        avg_games_per_season = owner['Total_Games'] / owner['Seasons_Played']
        
        html_content += f"""
                <tr>
                    <td class="rank">#{i}</td>
                    <td class="owner-name">{owner['Owner']}</td>
                    <td>{owner['Seasons_Played']}</td>
                    <td class="record">{owner['Total_Wins']}-{owner['Total_Losses']}-{owner['Total_Ties']}</td>
                    <td><span class="win-pct {win_pct_class}">{owner['Win_Percentage']:.3f}</span></td>
                    <td>{owner['Total_Games']}</td>
                    <td>{avg_games_per_season:.1f}</td>
                </tr>"""
    
    html_content += f"""
            </tbody>
        </table>
        
        <h2>📈 Wins by Year Trends</h2>
        <p style="margin-bottom: 20px; color: #7f8c8d;">
            Interactive chart showing win trends over time. Only owners with 5+ seasons shown by default. 
            Use the dropdown to highlight a specific owner, or click legend items to show/hide additional owners.
        </p>
        <div style="margin-bottom: 15px;">
            <label for="teamHighlight" style="margin-right: 10px; font-weight: bold; color: #2c3e50;">Highlight Team:</label>
            <select id="teamHighlight" onchange="highlightTeam(this.value)" style="
                padding: 8px 12px; 
                border: 1px solid #bdc3c7; 
                border-radius: 4px; 
                background-color: white; 
                font-size: 14px; 
                color: #2c3e50;
                cursor: pointer;
                min-width: 200px;
            ">
                <option value="None">None (Show All)</option>
            </select>
        </div>
        <div style="background-color: white; padding: 20px; border-radius: 8px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); height: 500px;">
            <canvas id="winsChart"></canvas>
        </div>
        
        <h2>🎯 League Highlights</h2>
        <div class="highlights">
            <div class="highlight-card">
                <div class="highlight-title">🥇 Best Win Percentage</div>
                <div class="highlight-value">{stats['best_win_pct']['Owner']}</div>
                <div>{stats['best_win_pct']['Win_Percentage']:.3f} ({stats['best_win_pct']['Total_Wins']}-{stats['best_win_pct']['Total_Losses']}-{stats['best_win_pct']['Total_Ties']})</div>
            </div>
            
            <div class="highlight-card">
                <div class="highlight-title">📉 Lowest Win Percentage</div>
                <div class="highlight-value">{stats['worst_win_pct']['Owner']}</div>
                <div>{stats['worst_win_pct']['Win_Percentage']:.3f} ({stats['worst_win_pct']['Total_Wins']}-{stats['worst_win_pct']['Total_Losses']}-{stats['worst_win_pct']['Total_Ties']})</div>
            </div>
            
            <div class="highlight-card">
                <div class="highlight-title">🏆 Most Career Wins</div>
                <div class="highlight-value">{stats['most_wins']['Owner']}</div>
                <div>{stats['most_wins']['Total_Wins']} wins in {stats['most_wins']['Seasons_Played']} seasons</div>
            </div>
            
            <div class="highlight-card">
                <div class="highlight-title">📈 Most Career Losses</div>
                <div class="highlight-value">{stats['most_losses']['Owner']}</div>
                <div>{stats['most_losses']['Total_Losses']} losses in {stats['most_losses']['Seasons_Played']} seasons</div>
            </div>
            
            <div class="highlight-card">
                <div class="highlight-title">⏱️ Most Experienced</div>
                <div class="highlight-value">{stats['most_seasons']['Owner']}</div>
                <div>{stats['most_seasons']['Seasons_Played']} seasons played</div>
            </div>
            
            <div class="highlight-card">
                <div class="highlight-title">🎯 League Average</div>
                <div class="highlight-value">{sum(o['Win_Percentage'] for o in standings) / len(standings):.3f}</div>
                <div>Average win percentage across all owners</div>
            </div>
        </div>
        
        <h2>📈 Performance Analysis</h2>
        <p><strong>Elite Performers (60%+ win rate):</strong> {len([o for o in standings if o['Win_Percentage'] >= 0.600])} owners</p>
        <p><strong>Above Average (55%+ win rate):</strong> {len([o for o in standings if o['Win_Percentage'] >= 0.550])} owners</p>
        <p><strong>At or Above .500:</strong> {len([o for o in standings if o['Win_Percentage'] >= 0.500])} owners</p>
        <p><strong>Below .500:</strong> {len([o for o in standings if o['Win_Percentage'] < 0.500])} owners</p>
        
        <div style="margin-top: 40px; padding-top: 20px; border-top: 2px solid #ecf0f1; text-align: center; color: #7f8c8d;">
            <p>📊 Report generated by Fantasy Basketball League Analytics System</p>
            <p>Data source: ownersStandingsOverall.csv</p>
        </div>
    </div>
    
    <script>
        // Table sorting functionality
        function sortTable(columnIndex, dataType = 'string') {{
            const table = document.querySelector('table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const headerRow = table.querySelector('thead tr');
            const headers = headerRow.querySelectorAll('th');
            const currentHeader = headers[columnIndex];
            
            // Determine sort direction BEFORE removing classes
            const isCurrentlyAsc = currentHeader.classList.contains('sort-asc');
            const isCurrentlyDesc = currentHeader.classList.contains('sort-desc');
            const isAscending = !isCurrentlyAsc; // If not currently ascending, make it ascending
            
            // Remove existing sort indicators from ALL headers
            headers.forEach(header => {{
                header.classList.remove('sort-asc', 'sort-desc');
                header.innerHTML = header.innerHTML.replace(/ [▲▼]/g, '');
            }});
            
            // Sort rows
            rows.sort((a, b) => {{
                let aValue = a.cells[columnIndex].textContent.trim();
                let bValue = b.cells[columnIndex].textContent.trim();
                
                // Handle different data types
                if (dataType === 'number') {{
                    aValue = parseFloat(aValue) || 0;
                    bValue = parseFloat(bValue) || 0;
                }} else if (dataType === 'percentage') {{
                    aValue = parseFloat(aValue) || 0;
                    bValue = parseFloat(bValue) || 0;
                }} else if (dataType === 'record') {{
                    // Extract wins from record (e.g., "107-63-1" -> 107)
                    const aWins = parseInt(aValue.split('-')[0]) || 0;
                    const bWins = parseInt(bValue.split('-')[0]) || 0;
                    aValue = aWins;
                    bValue = bWins;
                }}
                
                if (aValue < bValue) return isAscending ? -1 : 1;
                if (aValue > bValue) return isAscending ? 1 : -1;
                return 0;
            }});
            
            // Update table
            rows.forEach(row => tbody.appendChild(row));
            
            // Update rank column
            rows.forEach((row, index) => {{
                row.cells[0].textContent = `#${{index + 1}}`;
            }});
            
            // Add sort indicator
            const indicator = isAscending ? ' ▲' : ' ▼';
            currentHeader.innerHTML += indicator;
            currentHeader.classList.add(isAscending ? 'sort-asc' : 'sort-desc');
        }}
        
        // Add click handlers to table headers
        document.addEventListener('DOMContentLoaded', function() {{
            const headers = document.querySelectorAll('th');
            headers.forEach((header, index) => {{
                if (index === 0) return; // Skip rank column
                
                header.style.cursor = 'pointer';
                header.style.userSelect = 'none';
                header.title = 'Click to sort';
                
                const dataType = index === 2 ? 'number' :  // Seasons
                               index === 3 ? 'record' :   // Record  
                               index === 4 ? 'percentage' : // Win %
                               index === 5 ? 'number' :   // Total Games
                               index === 6 ? 'number' :   // Avg Games/Season
                               'string';                   // Owner name
                
                header.addEventListener('click', () => sortTable(index, dataType));
            }});
        }});
        
        // Chart data
        const chartData = {json.dumps(chart_data)};
        
        // Create the chart
        const ctx = document.getElementById('winsChart').getContext('2d');
        const winsChart = new Chart(ctx, {{
            type: 'line',
            data: chartData,
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    title: {{
                        display: true,
                        text: 'Wins by Year Trends (Veterans: 5+ Seasons)',
                        font: {{
                            size: 16,
                            weight: 'bold'
                        }}
                    }},
                    legend: {{
                        display: true,
                        position: 'bottom',
                        labels: {{
                            usePointStyle: true,
                            padding: 10,
                            fontSize: 12
                        }}
                    }},
                    tooltip: {{
                        mode: 'index',
                        intersect: false,
                        callbacks: {{
                            title: function(context) {{
                                return 'Year: ' + context[0].label;
                            }},
                            label: function(context) {{
                                if (context.parsed.y === null) {{
                                    return context.dataset.label + ': Did not play';
                                }}
                                return context.dataset.label + ': ' + context.parsed.y + ' wins';
                            }}
                        }}
                    }}
                }},
                interaction: {{
                    mode: 'index',
                    intersect: false,
                }},
                scales: {{
                    x: {{
                        display: true,
                        title: {{
                            display: true,
                            text: 'Year',
                            font: {{
                                size: 14,
                                weight: 'bold'
                            }}
                        }},
                        grid: {{
                            display: true,
                            color: 'rgba(0,0,0,0.1)'
                        }}
                    }},
                    y: {{
                        display: true,
                        title: {{
                            display: true,
                            text: 'Wins',
                            font: {{
                                size: 14,
                                weight: 'bold'
                            }}
                        }},
                        beginAtZero: true,
                        grid: {{
                            display: true,
                            color: 'rgba(0,0,0,0.1)'
                        }}
                    }}
                }},
                elements: {{
                    point: {{
                        radius: 4,
                        hoverRadius: 6
                    }},
                    line: {{
                        borderWidth: 2,
                        hoverBorderWidth: 3
                    }}
                }}
            }}
        }});
        
        // Store original colors for highlight effects
        winsChart.data.datasets.forEach(dataset => {{
            dataset.originalBorderColor = dataset.borderColor;
            dataset.originalBackgroundColor = dataset.backgroundColor;
        }});
        
        // Function to highlight a specific team
        function highlightTeam(teamName) {{
            const datasets = winsChart.data.datasets;
            
            if (teamName === 'None' || teamName === '') {{
                // Reset all lines to original state
                datasets.forEach((dataset) => {{
                    dataset.borderWidth = 2;
                    dataset.pointRadius = 4;
                    dataset.pointHoverRadius = 6;
                    // Restore original colors
                    if (dataset.originalBorderColor) {{
                        dataset.borderColor = dataset.originalBorderColor;
                        dataset.backgroundColor = dataset.originalBackgroundColor;
                    }}
                }});
            }} else {{
                // Highlight selected team and dim others
                datasets.forEach((dataset) => {{
                    if (dataset.label === teamName) {{
                        // Highlight the selected team
                        dataset.borderWidth = 4;
                        dataset.pointRadius = 6;
                        dataset.pointHoverRadius = 8;
                        // Restore original color
                        if (dataset.originalBorderColor) {{
                            dataset.borderColor = dataset.originalBorderColor;
                            dataset.backgroundColor = dataset.originalBackgroundColor;
                        }}
                    }} else {{
                        // Dim other teams
                        dataset.borderWidth = 1;
                        dataset.pointRadius = 2;
                        dataset.pointHoverRadius = 4;
                        // Apply gray color
                        dataset.borderColor = 'rgba(150, 150, 150, 0.3)';
                        dataset.backgroundColor = 'rgba(150, 150, 150, 0.1)';
                    }}
                }});
            }}
            
            winsChart.update('none');
        }}
        
        // Populate the dropdown with team names
        const teamSelect = document.getElementById('teamHighlight');
        const allTeams = winsChart.data.datasets.map(dataset => dataset.label).sort();
        
        allTeams.forEach(teamName => {{
            const option = document.createElement('option');
            option.value = teamName;
            option.textContent = teamName;
            teamSelect.appendChild(option);
        }});
    </script>
</body>
</html>"""
    
    return html_content

def main():
    """Main function to generate the report"""
    print("Generating Fantasy Basketball League Overall Standings Report...")
    
    try:
        # Read data
        standings = read_overall_standings()
        print(f"Loaded standings for {len(standings)} owners")
        
        # Read detailed data for chart
        detailed_standings = read_detailed_standings()
        print(f"Loaded detailed data: {len(detailed_standings)} records")
        
        # Prepare chart data
        chart_data = prepare_chart_data(detailed_standings)
        print(f"Prepared chart data for {len(chart_data['datasets'])} owners")
        
        # Calculate statistics
        stats = calculate_additional_stats(standings)
        
        # Generate HTML
        html_content = generate_html_report(standings, stats, chart_data)
        
        # Write to file
        output_path = Path(__file__).parent / '../StandingsReport.html'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Report generated successfully: {output_path}")
        print(f"📊 Report includes {len(standings)} owners across {stats['total_seasons']} total seasons")
        print(f"🏆 Best performer: {stats['best_win_pct']['Owner']} ({stats['best_win_pct']['Win_Percentage']:.3f})")
        
    except FileNotFoundError:
        print("❌ Error: ownersStandingsOverall.csv not found")
        print("Please run the data pipeline first: python3 data_pipeline.py")
    except Exception as e:
        print(f"❌ Error generating report: {e}")

if __name__ == "__main__":
    main()