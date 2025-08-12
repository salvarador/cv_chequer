#!/usr/bin/env python3
"""
Example script demonstrating how to use the CV Chequer API.
Shows how to interact with all available endpoints.
"""

import requests
import json
import os
from pathlib import Path

# API Configuration
API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint."""
    print("🔍 Testing health check...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API is healthy: {data['message']}")
            print(f"   Version: {data['version']}")
            if 'aws_identity' in data:
                print(f"   AWS Identity: {data['aws_identity']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running.")
        return False
    except Exception as e:
        print(f"❌ Error during health check: {e}")
        return False
    
    return True

def test_cv_analysis():
    """Test CV analysis endpoint."""
    print("\n📄 Testing CV analysis...")
    
    # Look for sample CV files
    cv_dir = Path("CV_FullStack/EPAM")
    if not cv_dir.exists():
        print("❌ Sample CV directory not found. Skipping CV analysis test.")
        return
    
    # Get first PDF file
    pdf_files = list(cv_dir.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found in sample directory. Skipping CV analysis test.")
        return
    
    sample_cv = pdf_files[0]
    print(f"   Using sample CV: {sample_cv.name}")
    
    try:
        with open(sample_cv, 'rb') as file:
            files = {'file': (sample_cv.name, file, 'application/pdf')}
            data = {'include_raw_text': 'false'}
            
            response = requests.post(
                f"{API_BASE_URL}/analyze-cv",
                files=files,
                data=data
            )
        
        if response.status_code == 200:
            result = response.json()
            analysis = result['analysis']
            print(f"✅ CV analysis successful!")
            print(f"   Candidate: {analysis['name']}")
            print(f"   Experience: {analysis['years_of_experience']}")
            
            # Count technologies
            tech_count = 0
            tech = analysis['technologies']
            tech_count += len(tech.get('programming_languages', []))
            tech_count += len(tech.get('databases', []))
            tech_count += len(tech.get('devops', []))
            tech_count += len(tech.get('others', []))
            
            # Count cloud services
            cloud = tech.get('cloud_services', {})
            for provider in ['aws', 'azure', 'gcp', 'others']:
                tech_count += len(cloud.get(provider, []))
            
            print(f"   Technologies found: {tech_count}")
            
            # Count soft skills
            skills_count = 0
            skills = analysis['soft_skills']
            for category in skills.values():
                skills_count += len(category)
            
            print(f"   Soft skills found: {skills_count}")
            
        else:
            print(f"❌ CV analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
    
    except Exception as e:
        print(f"❌ Error during CV analysis: {e}")

def test_job_description_analysis():
    """Test job description analysis endpoint."""
    print("\n💼 Testing job description analysis...")
    
    # Sample job description
    job_description = """
    Senior Full Stack Developer
    
    We are looking for an experienced Senior Full Stack Developer to join our team.
    
    Requirements:
    - 5+ years of software development experience
    - Strong proficiency in Python and JavaScript
    - Experience with React and FastAPI
    - Knowledge of AWS services (EC2, S3, Lambda)
    - Experience with PostgreSQL or MySQL
    - Docker and Kubernetes experience
    - Strong communication and leadership skills
    - Ability to work in agile environments
    
    Nice to have:
    - Experience with microservices architecture
    - Knowledge of Azure or GCP
    - DevOps experience with CI/CD pipelines
    """
    
    try:
        payload = {"job_description": job_description}
        response = requests.post(
            f"{API_BASE_URL}/analyze-job-description",
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            analysis = result['analysis']
            print(f"✅ Job description analysis successful!")
            print(f"   Job Title: {analysis['job_title']}")
            print(f"   Seniority: {analysis['seniority_level']}")
            print(f"   Experience Required: {analysis['experience_required']}")
            
            # Count requirements
            req_tech = analysis['required_technologies']
            tech_count = (
                len(req_tech.get('programming_languages', [])) +
                len(req_tech.get('databases', [])) +
                len(req_tech.get('devops', [])) +
                len(req_tech.get('others', []))
            )
            
            cloud = req_tech.get('cloud_services', {})
            for provider in ['aws', 'azure', 'gcp', 'others']:
                tech_count += len(cloud.get(provider, []))
            
            print(f"   Technology requirements: {tech_count}")
            
            req_skills = analysis['required_soft_skills']
            skills_count = 0
            for category in req_skills.values():
                skills_count += len(category)
            
            print(f"   Soft skill requirements: {skills_count}")
            
        else:
            print(f"❌ Job description analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
    
    except Exception as e:
        print(f"❌ Error during job description analysis: {e}")

def test_cv_job_matching():
    """Test CV and job matching endpoint."""
    print("\n🎯 Testing CV-Job matching...")
    
    # Look for sample CV files
    cv_dir = Path("CV_FullStack/EPAM")
    if not cv_dir.exists():
        print("❌ Sample CV directory not found. Skipping CV-Job matching test.")
        return
    
    pdf_files = list(cv_dir.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found. Skipping CV-Job matching test.")
        return
    
    sample_cv = pdf_files[0]
    
    # Sample job description
    job_description = """
    Senior Python Developer
    
    We are seeking a Senior Python Developer with strong backend development skills.
    
    Requirements:
    - 4+ years of Python development experience
    - Experience with FastAPI or Django
    - Knowledge of AWS services
    - PostgreSQL experience
    - Docker containerization
    - Strong problem-solving skills
    - Team collaboration experience
    """
    
    try:
        with open(sample_cv, 'rb') as file:
            files = {'file': (sample_cv.name, file, 'application/pdf')}
            data = {'job_description': job_description}
            
            response = requests.post(
                f"{API_BASE_URL}/match-cv-job",
                files=files,
                data=data
            )
        
        if response.status_code == 200:
            result = response.json()
            match_analysis = result['match_analysis']
            print(f"✅ CV-Job matching successful!")
            print(f"   Candidate: {match_analysis['candidate_name']}")
            print(f"   Overall Score: {match_analysis['overall_score']}%")
            print(f"   Technology Match: {match_analysis['technology_match']['score']}%")
            print(f"   Soft Skills Match: {match_analysis['soft_skills_match']['score']}%")
            print(f"   Experience Match: {match_analysis['experience_match']['score']}%")
            
        else:
            print(f"❌ CV-Job matching failed: {response.status_code}")
            print(f"   Response: {response.text}")
    
    except Exception as e:
        print(f"❌ Error during CV-Job matching: {e}")

def test_batch_cv_analysis():
    """Test batch CV analysis endpoint."""
    print("\n📚 Testing batch CV analysis...")
    
    # Look for sample CV files
    cv_dir = Path("CV_FullStack/EPAM")
    if not cv_dir.exists():
        print("❌ Sample CV directory not found. Skipping batch analysis test.")
        return
    
    pdf_files = list(cv_dir.glob("*.pdf"))[:3]  # Limit to 3 files for testing
    if not pdf_files:
        print("❌ No PDF files found. Skipping batch analysis test.")
        return
    
    print(f"   Analyzing {len(pdf_files)} CVs...")
    
    try:
        files = []
        for pdf_file in pdf_files:
            files.append(('files', (pdf_file.name, open(pdf_file, 'rb'), 'application/pdf')))
        
        response = requests.post(
            f"{API_BASE_URL}/batch-analyze-cvs",
            files=files
        )
        
        # Close opened files
        for _, (_, file_obj, _) in files:
            file_obj.close()
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Batch CV analysis successful!")
            print(f"   Total files: {result['total_files']}")
            print(f"   Successful: {result['successful_analyses']}")
            print(f"   Failed: {result['failed_analyses']}")
            
            if result['results']:
                print("   Candidates analyzed:")
                for analysis in result['results'][:3]:  # Show first 3
                    name = analysis.get('name', 'Unknown')
                    exp = analysis.get('years_of_experience', 'Unknown')
                    print(f"     - {name} ({exp})")
            
        else:
            print(f"❌ Batch CV analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
    
    except Exception as e:
        print(f"❌ Error during batch CV analysis: {e}")

def main():
    """Run all API tests."""
    print("🧪 CV Chequer API Test Suite")
    print("=" * 50)
    
    # Test health check first
    if not test_health_check():
        print("\n❌ API is not accessible. Please start the server first:")
        print("   python start_api.py")
        return
    
    # Run other tests
    test_cv_analysis()
    test_job_description_analysis()
    test_cv_job_matching()
    test_batch_cv_analysis()
    
    print("\n" + "=" * 50)
    print("🎉 API testing completed!")
    print("\n💡 To explore the API interactively, visit:")
    print(f"   📚 Swagger UI: {API_BASE_URL}/docs")
    print(f"   📖 ReDoc: {API_BASE_URL}/redoc")

if __name__ == "__main__":
    main()
