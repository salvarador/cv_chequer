#!/usr/bin/env python3
"""
Command-line interface for CV-job matching.
"""

import sys
import os
import argparse

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from backend.core.job_matcher import JobMatcher


def main():
    parser = argparse.ArgumentParser(description='Compare CV with job description')
    parser.add_argument('cv_path', help='Path to the CV PDF file')
    parser.add_argument('--job-file', '-j', help='Path to job description text file')
    parser.add_argument('--job-text', '-t', help='Job description text directly')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.cv_path):
        print(f"Error: CV file {args.cv_path} does not exist")
        return 1
    
    # Get job description
    job_description = ""
    if args.job_file:
        if os.path.exists(args.job_file):
            with open(args.job_file, 'r', encoding='utf-8') as f:
                job_description = f.read()
        else:
            print(f"Error: Job description file {args.job_file} does not exist")
            return 1
    elif args.job_text:
        job_description = args.job_text
    else:
        print("Please provide job description via --job-file or --job-text")
        print("\nInteractive mode - enter job description:")
        print("(Type 'END' on a new line to finish)")
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == 'END':
                    break
                lines.append(line)
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                return 1
        job_description = '\n'.join(lines)
    
    if not job_description.strip():
        print("Error: No job description provided")
        return 1
    
    try:
        # Perform comparison
        matcher = JobMatcher()
        results = matcher.compare_cv_with_job(args.cv_path, job_description)
        
        # Save results
        if results:
            output_file = f"match_results_{os.path.basename(args.cv_path).replace('.pdf', '')}.json"
            with open(output_file, 'w') as f:
                import json
                json.dump(results, f, indent=2)
            print(f"\nResults saved to {output_file}")
        
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
