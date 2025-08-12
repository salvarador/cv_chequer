#!/usr/bin/env python3

import json
from typing import Dict, List, Any, Tuple
from tabulate import tabulate
from .cv_analyzer import CVAnalyzer
from .config import get_aws_session, BEDROCK_MODEL_ID
import os
import argparse


class JobMatcher:
    def __init__(self):
        """Initialize the job matcher with AWS Bedrock client"""
        try:
            self.session = get_aws_session()
            self.bedrock_client = self.session.client('bedrock-runtime')
            self.cv_analyzer = CVAnalyzer()
            print("✓ Job Matcher initialized successfully")
        except Exception as e:
            print(f"✗ Failed to initialize Job Matcher: {e}")
            raise

    def analyze_job_description(self, job_description: str) -> Dict[str, Any]:
        """Analyze job description to extract requirements"""
        
        prompt = f"""
        Analyze the following job description and extract the requirements in JSON format.
        
        Job Description:
        {job_description}
        
        Please extract and organize the following information:
        1. Job title and seniority level
        2. Required technologies categorized as:
           - Programming Languages (with importance level 1-5)
           - Cloud Services (subdivided by provider: AWS, Azure, GCP, etc.)
           - Databases (with importance level 1-5)
           - DevOps tools (with importance level 1-5)
           - Others (frameworks, libraries, etc.)
        3. Required soft skills categorized as:
           - Leadership & Management
           - Communication & Collaboration
           - Problem Solving & Analytical Thinking
           - Adaptability & Learning
           - Time Management & Organization
           - Creativity & Innovation
           - Interpersonal Skills
           - Others
        4. Years of experience required
        5. Key responsibilities and nice-to-have skills
        
        For each requirement, provide an importance score (1-5):
        1 = Nice to have
        2 = Preferred
        3 = Important
        4 = Very Important
        5 = Critical/Must have
        
        Return ONLY a valid JSON object with this structure:
        {{
            "job_title": "Job Title",
            "seniority_level": "Junior/Mid/Senior/Lead",
            "experience_required": "X years",
            "required_technologies": {{
                "programming_languages": [
                    {{"name": "language", "importance": 5, "required": true}}
                ],
                "cloud_services": {{
                    "aws": [{{"name": "service", "importance": 4, "required": true}}],
                    "azure": [{{"name": "service", "importance": 3, "required": false}}],
                    "gcp": [{{"name": "service", "importance": 2, "required": false}}],
                    "others": [{{"name": "service", "importance": 3, "required": false}}]
                }},
                "databases": [
                    {{"name": "database", "importance": 4, "required": true}}
                ],
                "devops": [
                    {{"name": "tool", "importance": 3, "required": false}}
                ],
                "others": [
                    {{"name": "technology", "importance": 2, "required": false}}
                ]
            }},
            "required_soft_skills": {{
                "leadership_management": [
                    {{"skill": "Team Leadership", "importance": 4, "required": true}}
                ],
                "communication_collaboration": [
                    {{"skill": "Cross-functional Collaboration", "importance": 5, "required": true}}
                ],
                "problem_solving_analytical": [
                    {{"skill": "Complex Problem Solving", "importance": 4, "required": true}}
                ],
                "adaptability_learning": [
                    {{"skill": "Quick Learning", "importance": 3, "required": false}}
                ],
                "time_management_organization": [
                    {{"skill": "Project Management", "importance": 3, "required": false}}
                ],
                "creativity_innovation": [
                    {{"skill": "Innovative Solutions", "importance": 2, "required": false}}
                ],
                "interpersonal": [
                    {{"skill": "Client Relations", "importance": 3, "required": false}}
                ],
                "others": [
                    {{"skill": "Other relevant skill", "importance": 2, "required": false}}
                ]
            }},
            "key_responsibilities": [
                "Main responsibility 1",
                "Main responsibility 2"
            ],
            "nice_to_have": [
                "Additional skill 1",
                "Additional skill 2"
            ]
        }}
        """

        try:
            # Prepare the request for Claude
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }

            response = self.bedrock_client.invoke_model(
                modelId=BEDROCK_MODEL_ID,
                body=json.dumps(body)
            )

            response_body = json.loads(response['body'].read())
            analysis_result = response_body['content'][0]['text']
            
            # Try to parse the JSON response
            try:
                return json.loads(analysis_result)
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract JSON from the response
                start_idx = analysis_result.find('{')
                end_idx = analysis_result.rfind('}') + 1
                if start_idx != -1 and end_idx != 0:
                    json_str = analysis_result[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    raise ValueError("Could not extract valid JSON from response")

        except Exception as e:
            print(f"Error analyzing job description with Bedrock: {str(e)}")
            return {}

    def calculate_match_score(self, cv_data: Dict[str, Any], job_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate detailed match score between CV and job requirements"""
        
        # Initialize scores
        tech_matches = {"matched": [], "missing": [], "score": 0}
        soft_skill_matches = {"matched": [], "missing": [], "score": 0}
        
        # Get CV technologies and soft skills
        cv_technologies = cv_data.get('technologies', {})
        cv_soft_skills = cv_data.get('soft_skills', {})
        
        # Get job requirements
        job_tech_requirements = job_requirements.get('required_technologies', {})
        job_soft_requirements = job_requirements.get('required_soft_skills', {})
        
        # Calculate technology match
        tech_matches = self._calculate_technology_match(cv_technologies, job_tech_requirements)
        
        # Calculate soft skills match
        soft_skill_matches = self._calculate_soft_skills_match(cv_soft_skills, job_soft_requirements)
        
        # Calculate overall experience match
        experience_match = self._calculate_experience_match(
            cv_data.get('years_of_experience', '0 years'),
            job_requirements.get('experience_required', '0 years')
        )
        
        # Calculate weighted overall score
        # Technology: 50%, Soft Skills: 30%, Experience: 20%
        overall_score = (
            tech_matches['score'] * 0.5 +
            soft_skill_matches['score'] * 0.3 +
            experience_match['score'] * 0.2
        )
        
        return {
            "overall_score": round(overall_score, 1),
            "technology_match": tech_matches,
            "soft_skills_match": soft_skill_matches,
            "experience_match": experience_match,
            "candidate_name": cv_data.get('name', 'Unknown'),
            "job_title": job_requirements.get('job_title', 'Unknown Position')
        }

    def _calculate_technology_match(self, cv_tech: Dict, job_tech: Dict) -> Dict[str, Any]:
        """Calculate technology match score"""
        matched = []
        missing = []
        total_importance = 0
        matched_importance = 0
        
        # Create a flat list of CV technologies for easier searching
        cv_tech_list = []
        
        # Programming languages
        for lang in cv_tech.get('programming_languages', []):
            cv_tech_list.append(lang.get('name', '').lower())
        
        # Cloud services
        cloud_services = cv_tech.get('cloud_services', {})
        for provider, services in cloud_services.items():
            for service in services:
                cv_tech_list.append(service.get('name', '').lower())
        
        # Databases
        for db in cv_tech.get('databases', []):
            cv_tech_list.append(db.get('name', '').lower())
        
        # DevOps
        for tool in cv_tech.get('devops', []):
            cv_tech_list.append(tool.get('name', '').lower())
        
        # Others
        for tech in cv_tech.get('others', []):
            cv_tech_list.append(tech.get('name', '').lower())
        
        # Check each job requirement
        for category, requirements in job_tech.items():
            if category == 'cloud_services':
                # Handle cloud services nested structure
                for provider, services in requirements.items():
                    for req in services:
                        req_name = req.get('name', '').lower()
                        importance = req.get('importance', 3)
                        total_importance += importance
                        
                        if any(req_name in cv_tech.lower() for cv_tech in cv_tech_list):
                            matched.append({
                                "name": req.get('name', ''),
                                "category": f"{provider.upper()} Cloud",
                                "importance": importance,
                                "cv_probability": self._find_cv_tech_probability(cv_tech, req.get('name', ''))
                            })
                            matched_importance += importance
                        else:
                            missing.append({
                                "name": req.get('name', ''),
                                "category": f"{provider.upper()} Cloud",
                                "importance": importance,
                                "required": req.get('required', False)
                            })
            else:
                # Handle other categories
                for req in requirements:
                    req_name = req.get('name', '').lower()
                    importance = req.get('importance', 3)
                    total_importance += importance
                    
                    if any(req_name in cv_tech.lower() for cv_tech in cv_tech_list):
                        matched.append({
                            "name": req.get('name', ''),
                            "category": category.replace('_', ' ').title(),
                            "importance": importance,
                            "cv_probability": self._find_cv_tech_probability(cv_tech, req.get('name', ''))
                        })
                        matched_importance += importance
                    else:
                        missing.append({
                            "name": req.get('name', ''),
                            "category": category.replace('_', ' ').title(),
                            "importance": importance,
                            "required": req.get('required', False)
                        })
        
        score = (matched_importance / total_importance * 100) if total_importance > 0 else 0
        
        return {
            "matched": matched,
            "missing": missing,
            "score": round(score, 1),
            "matched_count": len(matched),
            "total_requirements": len(matched) + len(missing)
        }

    def _calculate_soft_skills_match(self, cv_skills: Dict, job_skills: Dict) -> Dict[str, Any]:
        """Calculate soft skills match score"""
        matched = []
        missing = []
        total_importance = 0
        matched_importance = 0
        
        # Create a flat list of CV soft skills for easier searching
        cv_skills_list = []
        for category, skills in cv_skills.items():
            for skill in skills:
                cv_skills_list.append(skill.get('skill', '').lower())
        
        # Check each job requirement
        for category, requirements in job_skills.items():
            for req in requirements:
                req_name = req.get('skill', '').lower()
                importance = req.get('importance', 3)
                total_importance += importance
                
                # Check if skill exists in CV (fuzzy matching)
                skill_found = False
                cv_confidence = 0
                
                for cv_skill in cv_skills_list:
                    if req_name in cv_skill or cv_skill in req_name or self._similar_skills(req_name, cv_skill):
                        skill_found = True
                        cv_confidence = self._find_cv_skill_confidence(cv_skills, req.get('skill', ''))
                        break
                
                if skill_found:
                    matched.append({
                        "skill": req.get('skill', ''),
                        "category": category.replace('_', ' ').title(),
                        "importance": importance,
                        "cv_confidence": cv_confidence
                    })
                    matched_importance += importance
                else:
                    missing.append({
                        "skill": req.get('skill', ''),
                        "category": category.replace('_', ' ').title(),
                        "importance": importance,
                        "required": req.get('required', False)
                    })
        
        score = (matched_importance / total_importance * 100) if total_importance > 0 else 0
        
        return {
            "matched": matched,
            "missing": missing,
            "score": round(score, 1),
            "matched_count": len(matched),
            "total_requirements": len(matched) + len(missing)
        }

    def _calculate_experience_match(self, cv_experience: str, required_experience: str) -> Dict[str, Any]:
        """Calculate experience match score"""
        import re
        
        # Extract numbers from experience strings
        cv_years = re.findall(r'\d+', cv_experience)
        req_years = re.findall(r'\d+', required_experience)
        
        cv_years_num = int(cv_years[0]) if cv_years else 0
        req_years_num = int(req_years[0]) if req_years else 0
        
        if req_years_num == 0:
            score = 100  # No specific requirement
        elif cv_years_num >= req_years_num:
            score = 100  # Meets or exceeds requirement
        else:
            # Partial score based on how close they are
            score = (cv_years_num / req_years_num * 100)
            score = min(score, 100)
        
        return {
            "cv_experience": cv_experience,
            "required_experience": required_experience,
            "score": round(score, 1),
            "meets_requirement": cv_years_num >= req_years_num
        }

    def _find_cv_tech_probability(self, cv_tech: Dict, tech_name: str) -> int:
        """Find the probability/authenticity score for a technology in CV"""
        tech_name_lower = tech_name.lower()
        
        # Search in all technology categories
        for category, items in cv_tech.items():
            if category == 'cloud_services':
                for provider, services in items.items():
                    for service in services:
                        if tech_name_lower in service.get('name', '').lower():
                            return service.get('probability', 0)
            else:
                for item in items:
                    if tech_name_lower in item.get('name', '').lower():
                        return item.get('probability', 0)
        return 0

    def _find_cv_skill_confidence(self, cv_skills: Dict, skill_name: str) -> int:
        """Find the confidence score for a soft skill in CV"""
        skill_name_lower = skill_name.lower()
        
        for category, skills in cv_skills.items():
            for skill in skills:
                if skill_name_lower in skill.get('skill', '').lower():
                    return skill.get('confidence', 0)
        return 0

    def _similar_skills(self, skill1: str, skill2: str) -> bool:
        """Check if two skills are similar (simple keyword matching)"""
        keywords1 = set(skill1.split())
        keywords2 = set(skill2.split())
        
        # If they share significant keywords, consider them similar
        intersection = keywords1.intersection(keywords2)
        return len(intersection) >= 1 and len(intersection) / min(len(keywords1), len(keywords2)) > 0.5

    def display_match_results(self, match_results: Dict[str, Any]) -> None:
        """Display the detailed match results in formatted tables"""
        
        print(f"\n{'='*80}")
        print(f"JOB MATCH ANALYSIS")
        print(f"{'='*80}")
        
        print(f"Candidate: {match_results['candidate_name']}")
        print(f"Position: {match_results['job_title']}")
        print(f"Overall Match Score: {match_results['overall_score']}%")
        
        # Overall scores summary
        print(f"\n{'-'*60}")
        print("SCORE BREAKDOWN")
        print(f"{'-'*60}")
        
        summary_data = [
            ["Technology Match", f"{match_results['technology_match']['score']}%", "50% weight"],
            ["Soft Skills Match", f"{match_results['soft_skills_match']['score']}%", "30% weight"],
            ["Experience Match", f"{match_results['experience_match']['score']}%", "20% weight"],
            ["OVERALL SCORE", f"{match_results['overall_score']}%", "100%"]
        ]
        
        print(tabulate(summary_data, headers=['Category', 'Score', 'Weight'], tablefmt='grid'))
        
        # Technology matches
        tech_match = match_results['technology_match']
        if tech_match['matched']:
            print(f"\n{'-'*60}")
            print(f"TECHNOLOGY MATCHES ({tech_match['matched_count']}/{tech_match['total_requirements']})")
            print(f"{'-'*60}")
            
            tech_data = []
            for match in tech_match['matched']:
                tech_data.append([
                    match['name'],
                    match['category'],
                    f"Importance: {match['importance']}/5",
                    f"CV Score: {match['cv_probability']}%"
                ])
            
            print(tabulate(tech_data, headers=['Technology', 'Category', 'Job Importance', 'CV Authenticity'], tablefmt='grid'))
        
        # Missing technologies
        if tech_match['missing']:
            print(f"\n{'-'*60}")
            print("MISSING TECHNOLOGIES")
            print(f"{'-'*60}")
            
            missing_tech_data = []
            for missing in tech_match['missing']:
                status = "REQUIRED" if missing['required'] else "Preferred"
                missing_tech_data.append([
                    missing['name'],
                    missing['category'],
                    f"Importance: {missing['importance']}/5",
                    status
                ])
            
            print(tabulate(missing_tech_data, headers=['Technology', 'Category', 'Job Importance', 'Status'], tablefmt='grid'))
        
        # Soft skills matches
        skill_match = match_results['soft_skills_match']
        if skill_match['matched']:
            print(f"\n{'-'*60}")
            print(f"SOFT SKILLS MATCHES ({skill_match['matched_count']}/{skill_match['total_requirements']})")
            print(f"{'-'*60}")
            
            skill_data = []
            for match in skill_match['matched']:
                skill_data.append([
                    match['skill'],
                    match['category'],
                    f"Importance: {match['importance']}/5",
                    f"CV Confidence: {match['cv_confidence']}%"
                ])
            
            print(tabulate(skill_data, headers=['Soft Skill', 'Category', 'Job Importance', 'CV Confidence'], tablefmt='grid'))
        
        # Missing soft skills
        if skill_match['missing']:
            print(f"\n{'-'*60}")
            print("MISSING SOFT SKILLS")
            print(f"{'-'*60}")
            
            missing_skill_data = []
            for missing in skill_match['missing']:
                status = "REQUIRED" if missing['required'] else "Preferred"
                missing_skill_data.append([
                    missing['skill'],
                    missing['category'],
                    f"Importance: {missing['importance']}/5",
                    status
                ])
            
            print(tabulate(missing_skill_data, headers=['Soft Skill', 'Category', 'Job Importance', 'Status'], tablefmt='grid'))
        
        # Experience analysis
        exp_match = match_results['experience_match']
        print(f"\n{'-'*60}")
        print("EXPERIENCE ANALYSIS")
        print(f"{'-'*60}")
        
        exp_data = [
            ["Candidate Experience", exp_match['cv_experience']],
            ["Required Experience", exp_match['required_experience']],
            ["Meets Requirement", "✓ Yes" if exp_match['meets_requirement'] else "✗ No"],
            ["Experience Score", f"{exp_match['score']}%"]
        ]
        
        print(tabulate(exp_data, headers=['Metric', 'Value'], tablefmt='grid'))
        
        print(f"\n{'='*80}")

    def compare_cv_with_job(self, cv_path: str, job_description: str) -> Dict[str, Any]:
        """Main method to compare CV with job description"""
        print(f"Analyzing CV: {cv_path}")
        print("Analyzing job description...")
        
        # Step 1: Analyze CV
        cv_data = self.cv_analyzer.analyze_cv(cv_path)
        if not cv_data:
            print("Failed to analyze CV")
            return {}
        
        # Step 2: Analyze job description
        job_requirements = self.analyze_job_description(job_description)
        if not job_requirements:
            print("Failed to analyze job description")
            return {}
        
        # Step 3: Calculate match
        match_results = self.calculate_match_score(cv_data, job_requirements)
        
        # Step 4: Display results
        self.display_match_results(match_results)
        
        return match_results


def main():
    parser = argparse.ArgumentParser(description='Compare CV with job description')
    parser.add_argument('cv_path', help='Path to the CV PDF file')
    parser.add_argument('--job-file', '-j', help='Path to job description text file')
    parser.add_argument('--job-text', '-t', help='Job description text directly')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.cv_path):
        print(f"Error: CV file {args.cv_path} does not exist")
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
    
    # Perform comparison
    matcher = JobMatcher()
    results = matcher.compare_cv_with_job(args.cv_path, job_description)
    
    # Save results
    if results:
        output_file = f"match_results_{os.path.basename(args.cv_path).replace('.pdf', '')}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {output_file}")


if __name__ == "__main__":
    main()
