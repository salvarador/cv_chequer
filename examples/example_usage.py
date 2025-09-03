#!/usr/bin/env python3
"""
Example usage of the CV Analyzer and Job Matcher
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.core.cv_analyzer import CVAnalyzer
from backend.core.batch_analyzer import BatchCVAnalyzer
from backend.core.job_matcher import JobMatcher
from backend.core.batch_job_matcher import BatchJobMatcher
import os


def analyze_single_cv():
    """Example: Analyze a single CV"""
    print("=== SINGLE CV ANALYSIS EXAMPLE ===")
    
    # Initialize analyzer
    analyzer = CVAnalyzer()
    
    # Example with one of the CVs in the directory
    cv_path = "data/CV_FullStack/EPAM/CV Brayan Urbina Gomez.pdf"
    
    if os.path.exists(cv_path):
        result = analyzer.analyze_cv(cv_path)
        print(f"Analysis completed for {cv_path}")
    else:
        print(f"CV file not found: {cv_path}")
        print("Available CVs:")
        for root, dirs, files in os.walk("data/CV_FullStack"):
            for file in files:
                if file.endswith('.pdf'):
                    print(f"  - {os.path.join(root, file)}")


def analyze_batch_cvs():
    """Example: Analyze multiple CVs in a directory"""
    print("\n=== BATCH CV ANALYSIS EXAMPLE ===")
    
    # Initialize batch analyzer
    batch_analyzer = BatchCVAnalyzer()
    
    # Analyze all CVs in a specific directory
    directory = "data/CV_FullStack/EPAM"
    
    if os.path.exists(directory):
        batch_analyzer.analyze_directory(directory)
        batch_analyzer.create_comparison_table()
        batch_analyzer.save_results("epam_cv_analysis.json")
    else:
        print(f"Directory not found: {directory}")


def job_match_single_cv():
    """Example: Match a single CV against a job description"""
    print("\n=== SINGLE CV JOB MATCHING EXAMPLE ===")
    
    # Initialize job matcher
    matcher = JobMatcher()
    
    # Example CV and job description
    cv_path = "data/CV_FullStack/EPAM/CV Brayan Urbina Gomez.pdf"
    job_desc_file = "examples/example_job_description.txt"
    
    if os.path.exists(cv_path) and os.path.exists(job_desc_file):
        with open(job_desc_file, 'r', encoding='utf-8') as f:
            job_description = f.read()
        
        result = matcher.compare_cv_with_job(cv_path, job_description)
        print(f"Job matching completed for {cv_path}")
    else:
        print(f"Files not found:")
        print(f"  CV: {cv_path} - {'✓' if os.path.exists(cv_path) else '✗'}")
        print(f"  Job Description: {job_desc_file} - {'✓' if os.path.exists(job_desc_file) else '✗'}")


def batch_job_matching():
    """Example: Match multiple CVs against a job description"""
    print("\n=== BATCH JOB MATCHING EXAMPLE ===")
    
    # Initialize batch job matcher
    batch_matcher = BatchJobMatcher()
    
    # Example directory and job description
    directory = "data/CV_FullStack/EPAM"
    job_desc_file = "examples/example_job_description.txt"
    
    if os.path.exists(directory) and os.path.exists(job_desc_file):
        with open(job_desc_file, 'r', encoding='utf-8') as f:
            job_description = f.read()
        
        batch_matcher.compare_multiple_cvs(directory, job_description)
        batch_matcher.create_ranking_table()
        batch_matcher.create_detailed_comparison()
        batch_matcher.create_top_candidates_summary(3)
        batch_matcher.save_results("batch_job_matching_results.json")
    else:
        print(f"Files not found:")
        print(f"  Directory: {directory} - {'✓' if os.path.exists(directory) else '✗'}")
        print(f"  Job Description: {job_desc_file} - {'✓' if os.path.exists(job_desc_file) else '✗'}")


def main():
    print("CV Analyzer & Job Matcher Examples")
    print("Make sure you have configured your AWS credentials!")
    print("Set the following environment variables:")
    print("- AWS_ACCESS_KEY_ID")
    print("- AWS_SECRET_ACCESS_KEY") 
    print("- AWS_REGION")
    print("- AWS_BEDROCK_MODEL_ID (optional)")
    
    choice = input("\nChoose analysis type:\n1. Single CV Analysis\n2. Batch CV Analysis\n3. Single CV Job Matching\n4. Batch Job Matching\n5. All Examples\nEnter choice (1-5): ")
    
    if choice == "1":
        analyze_single_cv()
    elif choice == "2":
        analyze_batch_cvs()
    elif choice == "3":
        job_match_single_cv()
    elif choice == "4":
        batch_job_matching()
    elif choice == "5":
        analyze_single_cv()
        analyze_batch_cvs()
        job_match_single_cv()
        batch_job_matching()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
