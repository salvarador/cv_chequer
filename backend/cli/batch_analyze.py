#!/usr/bin/env python3
"""
Command-line interface for batch CV analysis.
"""

import sys
import os
import argparse

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from backend.core.batch_analyzer import BatchCVAnalyzer


def main():
    parser = argparse.ArgumentParser(description='Batch analyze CVs in a directory')
    parser.add_argument('directory', help='Directory containing PDF files to analyze')
    parser.add_argument('--output', '-o', default='cv_analysis_results.json',
                       help='Output JSON file for results')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.directory):
        print(f"Error: Directory {args.directory} does not exist")
        return 1
    
    try:
        batch_analyzer = BatchCVAnalyzer()
        batch_analyzer.analyze_directory(args.directory)
        batch_analyzer.create_comparison_table()
        batch_analyzer.save_results(args.output)
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
