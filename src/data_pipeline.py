#!/usr/bin/env python3
"""
Data Pipeline for Fantasy Basketball League Analysis

This script runs the complete data processing pipeline in the correct order:
1. rawStandings.py - Parse HTML and create rawStandings.csv
2. owners.py - Generate owners mapping CSV
3. ownersStandings.py - Merge data and create both detailed and aggregated standings

Usage: python3 data_pipeline.py
"""

import subprocess
import sys
import os

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running: {script_name}")
    print(f"Description: {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        
        # Print the output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
            
        print(f"✓ {script_name} completed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error running {script_name}")
        print(f"Exit code: {e.returncode}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    print("Fantasy Basketball League Data Pipeline")
    print("=====================================")
    
    # Change to the src directory to ensure relative paths work
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Working directory: {os.getcwd()}")
    
    # Define the pipeline steps
    pipeline_steps = [
        ("rawStandings.py", "Parse HTML standings and create rawStandings.csv"),
        ("owners.py", "Generate team-to-owner mapping CSV"),
        ("ownersStandings.py", "Merge standings with owners and create aggregated data")
    ]
    
    # Track success of each step
    results = []
    
    # Run each step in the pipeline
    for script_name, description in pipeline_steps:
        success = run_script(script_name, description)
        results.append((script_name, success))
        
        if not success:
            print(f"\n❌ Pipeline failed at step: {script_name}")
            print("Stopping pipeline execution.")
            break
    else:
        # If we completed all steps without breaking
        print(f"\n{'='*60}")
        print("🎉 DATA PIPELINE COMPLETED SUCCESSFULLY!")
        print(f"{'='*60}")
        
        # Show final summary
        print("\nGenerated files:")
        data_files = [
            "../data/rawStandings.csv",
            "../data/owners.csv", 
            "../data/ownersStandings.csv",
            "../data/ownersStandingsOverall.csv"
        ]
        
        for file_path in data_files:
            if os.path.exists(file_path):
                print(f"  ✓ {file_path}")
            else:
                print(f"  ✗ {file_path} (missing)")
    
    # Print final summary
    print(f"\n{'='*60}")
    print("PIPELINE SUMMARY")
    print(f"{'='*60}")
    for script_name, success in results:
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"  {script_name}: {status}")

if __name__ == "__main__":
    main()