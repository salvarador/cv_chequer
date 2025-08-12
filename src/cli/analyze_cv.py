#!/usr/bin/env python3
"""
Command-line interface for single CV analysis.
"""

import sys
import os
import argparse

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.core.cv_analyzer import CVAnalyzer


def main():
    parser = argparse.ArgumentParser(description='Analyze CV using AWS Textract and Bedrock')
    parser.add_argument('pdf_path', help='Path to the PDF file to analyze')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.pdf_path):
        print(f"Error: File {args.pdf_path} does not exist")
        return 1
    
    try:
        analyzer = CVAnalyzer()
        analyzer.analyze_cv(args.pdf_path)
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
