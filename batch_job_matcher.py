#!/usr/bin/env python3

import os
import glob
import json
from job_matcher import JobMatcher
from tabulate import tabulate
from typing import List, Dict, Any
import argparse


class BatchJobMatcher:
    def __init__(self):
        self.matcher = JobMatcher()
        self.results = []

    def compare_multiple_cvs(self, cv_directory: str, job_description: str) -> List[Dict]:
        """Compare multiple CVs against a job description"""
        pdf_files = glob.glob(os.path.join(cv_directory, "**/*.pdf"), recursive=True)
        
        print(f"Found {len(pdf_files)} PDF files to analyze against job description...")
        
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"\n{'='*80}")
            print(f"Processing {i}/{len(pdf_files)}: {os.path.basename(pdf_file)}")
            print(f"{'='*80}")
            
            try:
                result = self.matcher.compare_cv_with_job(pdf_file, job_description)
                if result:
                    result['file_path'] = pdf_file
                    self.results.append(result)
            except Exception as e:
                print(f"Error processing {pdf_file}: {str(e)}")
                continue
        
        return self.results

    def create_ranking_table(self) -> None:
        """Create a ranking table of all candidates"""
        if not self.results:
            print("No results to display")
            return

        print(f"\n{'='*100}")
        print("CANDIDATE RANKING SUMMARY")
        print(f"{'='*100}")

        # Sort by overall score
        sorted_results = sorted(self.results, key=lambda x: x.get('overall_score', 0), reverse=True)

        # Create ranking table
        table_data = []
        for rank, result in enumerate(sorted_results, 1):
            table_data.append([
                rank,
                result.get('candidate_name', 'Unknown'),
                f"{result.get('overall_score', 0)}%",
                f"{result.get('technology_match', {}).get('score', 0)}%",
                f"{result.get('soft_skills_match', {}).get('score', 0)}%",
                f"{result.get('experience_match', {}).get('score', 0)}%",
                os.path.basename(result.get('file_path', 'Unknown'))
            ])

        print(tabulate(table_data, 
                      headers=['Rank', 'Candidate', 'Overall', 'Tech', 'Soft Skills', 'Experience', 'File'], 
                      tablefmt='grid'))

    def create_detailed_comparison(self) -> None:
        """Create detailed comparison tables"""
        if not self.results:
            return

        print(f"\n{'='*100}")
        print("DETAILED TECHNOLOGY COMPARISON")
        print(f"{'='*100}")

        # Collect all required technologies from job description
        if self.results:
            job_title = self.results[0].get('job_title', 'Unknown Position')
            print(f"Position: {job_title}")

        # Technology gaps analysis
        self._analyze_technology_gaps()
        
        # Soft skills gaps analysis
        self._analyze_soft_skills_gaps()

    def _analyze_technology_gaps(self) -> None:
        """Analyze technology gaps across all candidates"""
        print(f"\n{'-'*80}")
        print("TECHNOLOGY GAPS ANALYSIS")
        print(f"{'-'*80}")

        # Collect all missing technologies
        missing_tech_count = {}
        total_candidates = len(self.results)

        for result in self.results:
            missing_techs = result.get('technology_match', {}).get('missing', [])
            for tech in missing_techs:
                tech_name = tech['name']
                if tech_name not in missing_tech_count:
                    missing_tech_count[tech_name] = {
                        'count': 0,
                        'importance': tech['importance'],
                        'category': tech['category'],
                        'required': tech['required']
                    }
                missing_tech_count[tech_name]['count'] += 1

        # Create table of most commonly missing technologies
        if missing_tech_count:
            table_data = []
            for tech_name, data in missing_tech_count.items():
                gap_percentage = (data['count'] / total_candidates) * 100
                status = "REQUIRED" if data['required'] else "Preferred"
                table_data.append([
                    tech_name,
                    data['category'],
                    f"{data['importance']}/5",
                    f"{data['count']}/{total_candidates}",
                    f"{gap_percentage:.1f}%",
                    status
                ])

            # Sort by gap percentage (descending)
            table_data.sort(key=lambda x: float(x[4].replace('%', '')), reverse=True)

            print(tabulate(table_data, 
                          headers=['Technology', 'Category', 'Importance', 'Missing', 'Gap %', 'Status'], 
                          tablefmt='grid'))
        else:
            print("No technology gaps found - all candidates have required technologies!")

    def _analyze_soft_skills_gaps(self) -> None:
        """Analyze soft skills gaps across all candidates"""
        print(f"\n{'-'*80}")
        print("SOFT SKILLS GAPS ANALYSIS")
        print(f"{'-'*80}")

        # Collect all missing soft skills
        missing_skills_count = {}
        total_candidates = len(self.results)

        for result in self.results:
            missing_skills = result.get('soft_skills_match', {}).get('missing', [])
            for skill in missing_skills:
                skill_name = skill['skill']
                if skill_name not in missing_skills_count:
                    missing_skills_count[skill_name] = {
                        'count': 0,
                        'importance': skill['importance'],
                        'category': skill['category'],
                        'required': skill['required']
                    }
                missing_skills_count[skill_name]['count'] += 1

        # Create table of most commonly missing soft skills
        if missing_skills_count:
            table_data = []
            for skill_name, data in missing_skills_count.items():
                gap_percentage = (data['count'] / total_candidates) * 100
                status = "REQUIRED" if data['required'] else "Preferred"
                table_data.append([
                    skill_name,
                    data['category'],
                    f"{data['importance']}/5",
                    f"{data['count']}/{total_candidates}",
                    f"{gap_percentage:.1f}%",
                    status
                ])

            # Sort by gap percentage (descending)
            table_data.sort(key=lambda x: float(x[4].replace('%', '')), reverse=True)

            print(tabulate(table_data, 
                          headers=['Soft Skill', 'Category', 'Importance', 'Missing', 'Gap %', 'Status'], 
                          tablefmt='grid'))
        else:
            print("No soft skills gaps found - all candidates have required skills!")

    def create_top_candidates_summary(self, top_n: int = 5) -> None:
        """Create a summary of top N candidates"""
        if not self.results:
            return

        print(f"\n{'='*100}")
        print(f"TOP {min(top_n, len(self.results))} CANDIDATES DETAILED SUMMARY")
        print(f"{'='*100}")

        # Sort by overall score
        sorted_results = sorted(self.results, key=lambda x: x.get('overall_score', 0), reverse=True)
        top_candidates = sorted_results[:top_n]

        for rank, candidate in enumerate(top_candidates, 1):
            print(f"\n{'-'*60}")
            print(f"RANK #{rank}: {candidate.get('candidate_name', 'Unknown')} - {candidate.get('overall_score', 0)}%")
            print(f"{'-'*60}")
            
            # Technology strengths
            tech_matches = candidate.get('technology_match', {}).get('matched', [])
            if tech_matches:
                print("Technology Strengths:")
                for tech in tech_matches[:5]:  # Show top 5
                    print(f"  ✓ {tech['name']} ({tech['category']}) - Importance: {tech['importance']}/5, CV Score: {tech['cv_probability']}%")
            
            # Soft skill strengths
            skill_matches = candidate.get('soft_skills_match', {}).get('matched', [])
            if skill_matches:
                print("Soft Skill Strengths:")
                for skill in skill_matches[:5]:  # Show top 5
                    print(f"  ✓ {skill['skill']} ({skill['category']}) - Importance: {skill['importance']}/5, CV Confidence: {skill['cv_confidence']}%")
            
            # Key gaps
            tech_missing = candidate.get('technology_match', {}).get('missing', [])
            required_missing = [tech for tech in tech_missing if tech.get('required', False)]
            if required_missing:
                print("Critical Technology Gaps:")
                for tech in required_missing:
                    print(f"  ✗ {tech['name']} ({tech['category']}) - Importance: {tech['importance']}/5 [REQUIRED]")
            
            skill_missing = candidate.get('soft_skills_match', {}).get('missing', [])
            required_skill_missing = [skill for skill in skill_missing if skill.get('required', False)]
            if required_skill_missing:
                print("Critical Soft Skill Gaps:")
                for skill in required_skill_missing:
                    print(f"  ✗ {skill['skill']} ({skill['category']}) - Importance: {skill['importance']}/5 [REQUIRED]")

    def save_results(self, output_file: str = "batch_job_match_results.json") -> None:
        """Save all results to JSON file"""
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nDetailed results saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Compare multiple CVs with job description')
    parser.add_argument('cv_directory', help='Directory containing CV PDF files')
    parser.add_argument('--job-file', '-j', help='Path to job description text file')
    parser.add_argument('--job-text', '-t', help='Job description text directly')
    parser.add_argument('--top', '-n', type=int, default=5, help='Number of top candidates to show detailed summary (default: 5)')
    parser.add_argument('--output', '-o', default='batch_job_match_results.json', help='Output JSON file for results')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.cv_directory):
        print(f"Error: Directory {args.cv_directory} does not exist")
        return
    
    # Get job description
    job_description = ""
    if args.job_file:
        if os.path.exists(args.job_file):
            with open(args.job_file, 'r', encoding='utf-8') as f:
                job_description = f.read()
        else:
            print(f"Error: Job description file {args.job_file} does not exist")
            return
    elif args.job_text:
        job_description = args.job_text
    else:
        print("Please provide job description via --job-file or --job-text")
        print("\nInteractive mode - enter job description:")
        print("(Type 'END' on a new line to finish)")
        lines = []
        while True:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        job_description = '\n'.join(lines)
    
    if not job_description.strip():
        print("Error: No job description provided")
        return
    
    # Perform batch comparison
    batch_matcher = BatchJobMatcher()
    batch_matcher.compare_multiple_cvs(args.cv_directory, job_description)
    batch_matcher.create_ranking_table()
    batch_matcher.create_detailed_comparison()
    batch_matcher.create_top_candidates_summary(args.top)
    batch_matcher.save_results(args.output)


if __name__ == "__main__":
    main()
