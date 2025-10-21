#!/usr/bin/env python3
"""
Unified script to generate both Fantasy Basketball and Fantasy Football reports
"""

import subprocess
import sys
import os
from pathlib import Path

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        print(f"✅ {description} completed successfully")
        if result.stdout.strip():
            # Print only the summary lines, not all the detailed output
            lines = result.stdout.strip().split('\n')
            summary_lines = [line for line in lines if any(keyword in line for keyword in 
                           ['Total records:', 'Years covered:', 'Sample data:', 'Report generated successfully:', 'Best performer:'])]
            for line in summary_lines:
                print(f"   {line}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}:")
        print(f"   {e.stderr}")
        return False
    return True

def main():
    """Main function to run all report generation scripts"""
    print("🏈🏀 Fantasy League Analytics Pipeline")
    print("=" * 50)
    
    # Change to src directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    scripts = [
        ("rawStandings.py", "Extracting Basketball League standings"),
        ("ownersStandings.py", "Merging Basketball owners and calculating stats"),
        ("StandingsReport.py", "Generating Basketball League report (index.html)"),
        ("fbStandings.py", "Extracting Football League standings"), 
        ("fbOwnersStandings.py", "Merging Football owners and calculating stats"),
        ("FootballReport.py", "Generating Football League report (fb_index.html)")
    ]
    
    success_count = 0
    for script, description in scripts:
        if run_script(script, description):
            success_count += 1
        else:
            print(f"\n❌ Pipeline failed at: {description}")
            sys.exit(1)
    
    print(f"\n🎉 Pipeline completed successfully!")
    print(f"✅ Generated {success_count}/{len(scripts)} reports")
    print(f"\n📁 Output files:")
    print(f"   🏀 Basketball League: ../index.html")
    print(f"   🏈 Football League: ../fb_index.html")
    print(f"\n🌐 View reports:")
    print(f"   Basketball: file://{Path('../index.html').resolve()}")
    print(f"   Football: file://{Path('../fb_index.html').resolve()}")

if __name__ == "__main__":
    main()