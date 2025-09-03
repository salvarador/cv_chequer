#!/usr/bin/env python3

import os
import glob
from .cv_analyzer import CVAnalyzer
import json
from tabulate import tabulate
from typing import List, Dict


class BatchCVAnalyzer:
    def __init__(self):
        self.analyzer = CVAnalyzer()
        self.results = []

    def analyze_directory(self, directory_path: str) -> List[Dict]:
        """Analyze all PDF files in a directory"""
        pdf_files = glob.glob(os.path.join(directory_path, "**/*.pdf"), recursive=True)
        
        print(f"Found {len(pdf_files)} PDF files to analyze...")
        
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"\n{'='*80}")
            print(f"Processing {i}/{len(pdf_files)}: {os.path.basename(pdf_file)}")
            print(f"{'='*80}")
            
            try:
                result = self.analyzer.analyze_cv(pdf_file)
                if result:
                    result['file_path'] = pdf_file
                    self.results.append(result)
            except Exception as e:
                print(f"Error processing {pdf_file}: {str(e)}")
                continue
        
        return self.results

    def create_comparison_table(self) -> None:
        """Create a comparison table of all analyzed CVs"""
        if not self.results:
            print("No results to display")
            return

        print(f"\n{'='*100}")
        print("CV COMPARISON SUMMARY")
        print(f"{'='*100}")

        # Basic info comparison
        table_data = []
        for result in self.results:
            table_data.append([
                result.get('name', 'Unknown'),
                result.get('years_of_experience', 'Unknown'),
                os.path.basename(result.get('file_path', 'Unknown'))
            ])

        print(tabulate(table_data, headers=['Name', 'Experience', 'File'], tablefmt='grid'))

        # Technology summary
        self.create_technology_summary()

    def create_technology_summary(self) -> None:
        """Create a summary of technologies across all CVs"""
        print(f"\n{'='*100}")
        print("TECHNOLOGY SUMMARY ACROSS ALL CVS")
        print(f"{'='*100}")

        # Collect all technologies
        all_languages = {}
        all_cloud = {}
        all_databases = {}
        all_devops = {}
        all_soft_skills = {}

        for result in self.results:
            name = result.get('name', 'Unknown')
            technologies = result.get('technologies', {})

            # Programming languages
            for lang in technologies.get('programming_languages', []):
                lang_name = lang.get('name', '')
                if lang_name not in all_languages:
                    all_languages[lang_name] = []
                all_languages[lang_name].append((name, lang.get('probability', 0)))

            # Cloud services
            cloud_services = technologies.get('cloud_services', {})
            for provider, services in cloud_services.items():
                for service in services:
                    service_name = f"{provider.upper()}: {service.get('name', '')}"
                    if service_name not in all_cloud:
                        all_cloud[service_name] = []
                    all_cloud[service_name].append((name, service.get('probability', 0)))

            # Databases
            for db in technologies.get('databases', []):
                db_name = db.get('name', '')
                if db_name not in all_databases:
                    all_databases[db_name] = []
                all_databases[db_name].append((name, db.get('probability', 0)))

            # DevOps
            for tool in technologies.get('devops', []):
                tool_name = tool.get('name', '')
                if tool_name not in all_devops:
                    all_devops[tool_name] = []
                all_devops[tool_name].append((name, tool.get('probability', 0)))

            # Soft Skills (aggregate all categories)
            soft_skills = result.get('soft_skills', {})
            for category, skills in soft_skills.items():
                for skill in skills:
                    skill_name = skill.get('skill', '')
                    if skill_name not in all_soft_skills:
                        all_soft_skills[skill_name] = []
                    all_soft_skills[skill_name].append((name, skill.get('confidence', 0)))

        # Display summaries
        self._display_technology_category("PROGRAMMING LANGUAGES", all_languages)
        self._display_technology_category("CLOUD SERVICES", all_cloud)
        self._display_technology_category("DATABASES", all_databases)
        self._display_technology_category("DEVOPS TOOLS", all_devops)
        self._display_soft_skills_category("SOFT SKILLS", all_soft_skills)

    def _display_technology_category(self, category_name: str, tech_dict: dict) -> None:
        """Display a specific technology category summary"""
        if not tech_dict:
            return

        print(f"\n{'-'*60}")
        print(f"{category_name}")
        print(f"{'-'*60}")

        table_data = []
        for tech_name, candidates in tech_dict.items():
            candidate_list = []
            avg_probability = 0
            for candidate, prob in candidates:
                candidate_list.append(f"{candidate} ({prob}%)")
                avg_probability += prob
            
            avg_probability = avg_probability / len(candidates) if candidates else 0
            
            table_data.append([
                tech_name,
                f"{avg_probability:.1f}%",
                len(candidates),
                "; ".join(candidate_list[:3])  # Show first 3 candidates
            ])

        # Sort by number of mentions
        table_data.sort(key=lambda x: x[2], reverse=True)

        print(tabulate(table_data, 
                      headers=['Technology', 'Avg Authenticity', 'Mentions', 'Candidates (First 3)'], 
                      tablefmt='grid'))

    def _display_soft_skills_category(self, category_name: str, skills_dict: dict) -> None:
        """Display soft skills category summary"""
        if not skills_dict:
            return

        print(f"\n{'-'*80}")
        print(f"{category_name}")
        print(f"{'-'*80}")

        table_data = []
        for skill_name, candidates in skills_dict.items():
            candidate_list = []
            avg_confidence = 0
            for candidate, confidence in candidates:
                candidate_list.append(f"{candidate} ({confidence}%)")
                avg_confidence += confidence
            
            avg_confidence = avg_confidence / len(candidates) if candidates else 0
            
            table_data.append([
                skill_name,
                f"{avg_confidence:.1f}%",
                len(candidates),
                "; ".join(candidate_list[:3])  # Show first 3 candidates
            ])

        # Sort by number of mentions
        table_data.sort(key=lambda x: x[2], reverse=True)

        print(tabulate(table_data, 
                      headers=['Soft Skill', 'Avg Confidence', 'Mentions', 'Candidates (First 3)'], 
                      tablefmt='grid'))

    def save_results(self, output_file: str = "cv_analysis_results.json") -> None:
        """Save results to JSON file"""
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nResults saved to {output_file}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch analyze CVs in a directory')
    parser.add_argument('directory', help='Directory containing PDF files to analyze')
    parser.add_argument('--output', '-o', default='cv_analysis_results.json',
                       help='Output JSON file for results')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.directory):
        print(f"Error: Directory {args.directory} does not exist")
        return
    
    batch_analyzer = BatchCVAnalyzer()
    batch_analyzer.analyze_directory(args.directory)
    batch_analyzer.create_comparison_table()
    batch_analyzer.save_results(args.output)


if __name__ == "__main__":
    main()
