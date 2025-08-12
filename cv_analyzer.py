import boto3
import json
import base64
from typing import Dict, List, Any
from tabulate import tabulate
import os
import argparse
from botocore.exceptions import ClientError, NoCredentialsError
from config import get_aws_session, BEDROCK_MODEL_ID
import pdfplumber
import PyPDF2
import io


class CVAnalyzer:
    def __init__(self):
        """Initialize AWS clients for Textract and Bedrock"""
        try:
            self.session = get_aws_session()
            self.textract_client = self.session.client('textract')
            self.bedrock_client = self.session.client('bedrock-runtime')
            print("✓ AWS clients initialized successfully")
        except Exception as e:
            print(f"✗ Failed to initialize AWS clients: {e}")
            raise

    def extract_text_with_pdfplumber(self, pdf_path: str) -> str:
        """Extract text from PDF using pdfplumber (fallback method)"""
        try:
            print(f"Using pdfplumber to extract text from {os.path.basename(pdf_path)}...")
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + '\n'
                    print(f"  Processed page {page_num}/{len(pdf.pages)}")
            
            print(f"✓ Successfully extracted {len(text)} characters with pdfplumber")
            return text
        except Exception as e:
            print(f"✗ pdfplumber extraction failed: {str(e)}")
            return ""

    def extract_text_with_pypdf2(self, pdf_path: str) -> str:
        """Extract text from PDF using PyPDF2 (fallback method)"""
        try:
            print(f"Using PyPDF2 to extract text from {os.path.basename(pdf_path)}...")
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + '\n'
                    print(f"  Processed page {page_num}/{len(pdf_reader.pages)}")
            
            print(f"✓ Successfully extracted {len(text)} characters with PyPDF2")
            return text
        except Exception as e:
            print(f"✗ PyPDF2 extraction failed: {str(e)}")
            return ""

    def validate_pdf_file(self, pdf_path: str) -> bool:
        """Validate if PDF file is readable"""
        try:
            with open(pdf_path, 'rb') as file:
                header = file.read(8)
                if not header.startswith(b'%PDF-'):
                    print(f"✗ File {pdf_path} is not a valid PDF file")
                    return False
            
            # Check file size (Textract has limits)
            file_size = os.path.getsize(pdf_path)
            max_size = 10 * 1024 * 1024  # 10MB limit for Textract
            
            if file_size > max_size:
                print(f"⚠ PDF file is {file_size / (1024*1024):.1f}MB (max 10MB for Textract)")
                print("Will use alternative extraction methods")
                return False
            
            print(f"✓ PDF file validation passed ({file_size / (1024*1024):.1f}MB)")
            return True
            
        except Exception as e:
            print(f"✗ PDF validation failed: {str(e)}")
            return False

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using multiple methods with fallbacks"""
        if not os.path.exists(pdf_path):
            print(f"✗ File not found: {pdf_path}")
            return ""
        
        # Validate PDF file
        is_valid_for_textract = self.validate_pdf_file(pdf_path)
        
        # Method 1: Try AWS Textract first (if file is suitable)
        if is_valid_for_textract:
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_bytes = file.read()

                print(f"Method 1: Extracting text with AWS Textract from {os.path.basename(pdf_path)}...")
                
                response = self.textract_client.detect_document_text(
                    Document={'Bytes': pdf_bytes}
                )

                # Extract text from response
                text = ""
                for block in response['Blocks']:
                    if block['BlockType'] == 'LINE':
                        text += block['Text'] + '\n'

                if text.strip():
                    print(f"✓ Successfully extracted {len(text)} characters with Textract")
                    return text
                else:
                    print("⚠ Textract returned empty text, trying fallback methods...")

            except ClientError as e:
                error_code = e.response['Error']['Code']
                error_message = e.response['Error']['Message']
                
                if error_code == 'UnsupportedDocumentException':
                    print(f"⚠ Textract doesn't support this PDF format: {error_message}")
                    print("Trying alternative extraction methods...")
                elif error_code == 'UnrecognizedClientException':
                    print(f"✗ AWS Authentication Error: {error_message}")
                    print("Please check your AWS credentials and try again.")
                    return ""
                elif error_code == 'AccessDeniedException':
                    print(f"✗ Access Denied: {error_message}")
                    print("Please ensure your AWS account has Textract permissions.")
                    return ""
                else:
                    print(f"⚠ AWS Textract Error [{error_code}]: {error_message}")
                    print("Trying alternative extraction methods...")
            
            except Exception as e:
                print(f"⚠ Unexpected error with Textract: {str(e)}")
                print("Trying alternative extraction methods...")

        # Method 2: Try pdfplumber
        text = self.extract_text_with_pdfplumber(pdf_path)
        if text.strip():
            return text

        # Method 3: Try PyPDF2
        text = self.extract_text_with_pypdf2(pdf_path)
        if text.strip():
            return text

        print("✗ All text extraction methods failed")
        return ""

    def analyze_cv_with_bedrock(self, cv_text: str) -> Dict[str, Any]:
        """Analyze CV text using AWS Bedrock"""
        
        prompt = f"""
        Analyze the following CV and extract the requested information in JSON format.
        
        CV Text:
        {cv_text}
        
        Please extract and organize the following information:
        1. Name of the candidate
        2. Years of experience (total professional experience)
        3. Technologies categorized as follows:
           - Programming Languages
           - Cloud Services (subdivided by provider: AWS, Azure, GCP, etc.)
           - Databases
           - DevOps tools
           - Others (frameworks, libraries, etc.)
        4. Soft Skills - Identify and categorize soft skills mentioned or implied in the CV
        
        For each technology mentioned, provide a probability percentage (0-100) of authentic usage based on:
        - How it's mentioned in context with projects/experience
        - Depth of description
        - Consistency with experience level
        - Professional context
        
        For soft skills, provide a confidence percentage (0-100) based on:
        - Direct mentions in CV
        - Evidence from project descriptions
        - Leadership roles or team experiences
        - Communication examples (presentations, documentation, etc.)
        - Problem-solving examples
        
        Soft skills categories to look for:
        - Leadership & Management
        - Communication & Collaboration
        - Problem Solving & Analytical Thinking
        - Adaptability & Learning
        - Time Management & Organization
        - Creativity & Innovation
        - Interpersonal Skills
        - Others
        
        Return ONLY a valid JSON object with this structure:
        {{
            "name": "candidate name",
            "years_of_experience": "X years",
            "technologies": {{
                "programming_languages": [
                    {{"name": "language", "probability": 85}}
                ],
                "cloud_services": {{
                    "aws": [{{"name": "service", "probability": 90}}],
                    "azure": [{{"name": "service", "probability": 75}}],
                    "gcp": [{{"name": "service", "probability": 80}}],
                    "others": [{{"name": "service", "probability": 70}}]
                }},
                "databases": [
                    {{"name": "database", "probability": 88}}
                ],
                "devops": [
                    {{"name": "tool", "probability": 92}}
                ],
                "others": [
                    {{"name": "technology", "probability": 85}}
                ]
            }},
            "soft_skills": {{
                "leadership_management": [
                    {{"skill": "Team Leadership", "confidence": 85, "evidence": "Led team of 5 developers"}}
                ],
                "communication_collaboration": [
                    {{"skill": "Cross-functional Collaboration", "confidence": 90, "evidence": "Worked with product and design teams"}}
                ],
                "problem_solving_analytical": [
                    {{"skill": "Complex Problem Solving", "confidence": 80, "evidence": "Resolved critical system issues"}}
                ],
                "adaptability_learning": [
                    {{"skill": "Quick Learning", "confidence": 75, "evidence": "Mastered new technologies rapidly"}}
                ],
                "time_management_organization": [
                    {{"skill": "Project Management", "confidence": 85, "evidence": "Delivered projects on time"}}
                ],
                "creativity_innovation": [
                    {{"skill": "Innovative Solutions", "confidence": 70, "evidence": "Developed novel approaches"}}
                ],
                "interpersonal": [
                    {{"skill": "Client Relations", "confidence": 80, "evidence": "Managed client communications"}}
                ],
                "others": [
                    {{"skill": "Other relevant skill", "confidence": 75, "evidence": "Supporting evidence"}}
                ]
            }}
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
            print(f"Error analyzing CV with Bedrock: {str(e)}")
            return {}

    def display_results(self, analysis: Dict[str, Any]) -> None:
        """Display the analysis results in a formatted table"""
        if not analysis:
            print("No analysis results to display")
            return

        print(f"\n{'='*80}")
        print(f"CV ANALYSIS RESULTS")
        print(f"{'='*80}")
        
        # Basic Information
        print(f"\nCandidate: {analysis.get('name', 'Unknown')}")
        print(f"Experience: {analysis.get('years_of_experience', 'Unknown')}")
        
        technologies = analysis.get('technologies', {})
        
        # Programming Languages
        if technologies.get('programming_languages'):
            print(f"\n{'-'*50}")
            print("PROGRAMMING LANGUAGES")
            print(f"{'-'*50}")
            
            table_data = []
            for lang in technologies['programming_languages']:
                table_data.append([
                    lang.get('name', 'Unknown'),
                    f"{lang.get('probability', 0)}%"
                ])
            
            print(tabulate(table_data, headers=['Language', 'Authenticity'], tablefmt='grid'))

        # Cloud Services
        cloud_services = technologies.get('cloud_services', {})
        if cloud_services:
            print(f"\n{'-'*50}")
            print("CLOUD SERVICES")
            print(f"{'-'*50}")
            
            for provider, services in cloud_services.items():
                if services:
                    print(f"\n{provider.upper()}:")
                    table_data = []
                    for service in services:
                        table_data.append([
                            service.get('name', 'Unknown'),
                            f"{service.get('probability', 0)}%"
                        ])
                    print(tabulate(table_data, headers=['Service', 'Authenticity'], tablefmt='grid'))

        # Databases
        if technologies.get('databases'):
            print(f"\n{'-'*50}")
            print("DATABASES")
            print(f"{'-'*50}")
            
            table_data = []
            for db in technologies['databases']:
                table_data.append([
                    db.get('name', 'Unknown'),
                    f"{db.get('probability', 0)}%"
                ])
            
            print(tabulate(table_data, headers=['Database', 'Authenticity'], tablefmt='grid'))

        # DevOps
        if technologies.get('devops'):
            print(f"\n{'-'*50}")
            print("DEVOPS TOOLS")
            print(f"{'-'*50}")
            
            table_data = []
            for tool in technologies['devops']:
                table_data.append([
                    tool.get('name', 'Unknown'),
                    f"{tool.get('probability', 0)}%"
                ])
            
            print(tabulate(table_data, headers=['Tool', 'Authenticity'], tablefmt='grid'))

        # Others
        if technologies.get('others'):
            print(f"\n{'-'*50}")
            print("OTHER TECHNOLOGIES")
            print(f"{'-'*50}")
            
            table_data = []
            for tech in technologies['others']:
                table_data.append([
                    tech.get('name', 'Unknown'),
                    f"{tech.get('probability', 0)}%"
                ])
            
            print(tabulate(table_data, headers=['Technology', 'Authenticity'], tablefmt='grid'))

        # Soft Skills
        soft_skills = analysis.get('soft_skills', {})
        if soft_skills:
            print(f"\n{'='*80}")
            print("SOFT SKILLS ANALYSIS")
            print(f"{'='*80}")
            
            # Leadership & Management
            if soft_skills.get('leadership_management'):
                print(f"\n{'-'*60}")
                print("LEADERSHIP & MANAGEMENT")
                print(f"{'-'*60}")
                
                table_data = []
                for skill in soft_skills['leadership_management']:
                    table_data.append([
                        skill.get('skill', 'Unknown'),
                        f"{skill.get('confidence', 0)}%",
                        skill.get('evidence', 'No evidence provided')[:50] + "..." if len(skill.get('evidence', '')) > 50 else skill.get('evidence', 'No evidence provided')
                    ])
                
                print(tabulate(table_data, headers=['Skill', 'Confidence', 'Evidence'], tablefmt='grid'))

            # Communication & Collaboration
            if soft_skills.get('communication_collaboration'):
                print(f"\n{'-'*60}")
                print("COMMUNICATION & COLLABORATION")
                print(f"{'-'*60}")
                
                table_data = []
                for skill in soft_skills['communication_collaboration']:
                    table_data.append([
                        skill.get('skill', 'Unknown'),
                        f"{skill.get('confidence', 0)}%",
                        skill.get('evidence', 'No evidence provided')[:50] + "..." if len(skill.get('evidence', '')) > 50 else skill.get('evidence', 'No evidence provided')
                    ])
                
                print(tabulate(table_data, headers=['Skill', 'Confidence', 'Evidence'], tablefmt='grid'))

            # Problem Solving & Analytical Thinking
            if soft_skills.get('problem_solving_analytical'):
                print(f"\n{'-'*60}")
                print("PROBLEM SOLVING & ANALYTICAL THINKING")
                print(f"{'-'*60}")
                
                table_data = []
                for skill in soft_skills['problem_solving_analytical']:
                    table_data.append([
                        skill.get('skill', 'Unknown'),
                        f"{skill.get('confidence', 0)}%",
                        skill.get('evidence', 'No evidence provided')[:50] + "..." if len(skill.get('evidence', '')) > 50 else skill.get('evidence', 'No evidence provided')
                    ])
                
                print(tabulate(table_data, headers=['Skill', 'Confidence', 'Evidence'], tablefmt='grid'))

            # Adaptability & Learning
            if soft_skills.get('adaptability_learning'):
                print(f"\n{'-'*60}")
                print("ADAPTABILITY & LEARNING")
                print(f"{'-'*60}")
                
                table_data = []
                for skill in soft_skills['adaptability_learning']:
                    table_data.append([
                        skill.get('skill', 'Unknown'),
                        f"{skill.get('confidence', 0)}%",
                        skill.get('evidence', 'No evidence provided')[:50] + "..." if len(skill.get('evidence', '')) > 50 else skill.get('evidence', 'No evidence provided')
                    ])
                
                print(tabulate(table_data, headers=['Skill', 'Confidence', 'Evidence'], tablefmt='grid'))

            # Time Management & Organization
            if soft_skills.get('time_management_organization'):
                print(f"\n{'-'*60}")
                print("TIME MANAGEMENT & ORGANIZATION")
                print(f"{'-'*60}")
                
                table_data = []
                for skill in soft_skills['time_management_organization']:
                    table_data.append([
                        skill.get('skill', 'Unknown'),
                        f"{skill.get('confidence', 0)}%",
                        skill.get('evidence', 'No evidence provided')[:50] + "..." if len(skill.get('evidence', '')) > 50 else skill.get('evidence', 'No evidence provided')
                    ])
                
                print(tabulate(table_data, headers=['Skill', 'Confidence', 'Evidence'], tablefmt='grid'))

            # Creativity & Innovation
            if soft_skills.get('creativity_innovation'):
                print(f"\n{'-'*60}")
                print("CREATIVITY & INNOVATION")
                print(f"{'-'*60}")
                
                table_data = []
                for skill in soft_skills['creativity_innovation']:
                    table_data.append([
                        skill.get('skill', 'Unknown'),
                        f"{skill.get('confidence', 0)}%",
                        skill.get('evidence', 'No evidence provided')[:50] + "..." if len(skill.get('evidence', '')) > 50 else skill.get('evidence', 'No evidence provided')
                    ])
                
                print(tabulate(table_data, headers=['Skill', 'Confidence', 'Evidence'], tablefmt='grid'))

            # Interpersonal Skills
            if soft_skills.get('interpersonal'):
                print(f"\n{'-'*60}")
                print("INTERPERSONAL SKILLS")
                print(f"{'-'*60}")
                
                table_data = []
                for skill in soft_skills['interpersonal']:
                    table_data.append([
                        skill.get('skill', 'Unknown'),
                        f"{skill.get('confidence', 0)}%",
                        skill.get('evidence', 'No evidence provided')[:50] + "..." if len(skill.get('evidence', '')) > 50 else skill.get('evidence', 'No evidence provided')
                    ])
                
                print(tabulate(table_data, headers=['Skill', 'Confidence', 'Evidence'], tablefmt='grid'))

            # Other Soft Skills
            if soft_skills.get('others'):
                print(f"\n{'-'*60}")
                print("OTHER SOFT SKILLS")
                print(f"{'-'*60}")
                
                table_data = []
                for skill in soft_skills['others']:
                    table_data.append([
                        skill.get('skill', 'Unknown'),
                        f"{skill.get('confidence', 0)}%",
                        skill.get('evidence', 'No evidence provided')[:50] + "..." if len(skill.get('evidence', '')) > 50 else skill.get('evidence', 'No evidence provided')
                    ])
                
                print(tabulate(table_data, headers=['Skill', 'Confidence', 'Evidence'], tablefmt='grid'))

        print(f"\n{'='*80}")

    def analyze_cv(self, pdf_path: str) -> Dict[str, Any]:
        """Main method to analyze a CV from PDF file"""
        print(f"Analyzing CV: {pdf_path}")
        
        # Step 1: Extract text from PDF
        print("Step 1: Extracting text from PDF...")
        cv_text = self.extract_text_from_pdf(pdf_path)
        
        if not cv_text:
            print("Failed to extract text from PDF")
            return {}
        
        # Step 2: Analyze with Bedrock
        print("Step 2: Analyzing CV with AWS Bedrock...")
        analysis = self.analyze_cv_with_bedrock(cv_text)
        
        # Step 3: Display results
        print("Step 3: Displaying results...")
        self.display_results(analysis)
        
        return analysis


def main():
    parser = argparse.ArgumentParser(description='Analyze CV using AWS Textract and Bedrock')
    parser.add_argument('pdf_path', help='Path to the PDF file to analyze')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.pdf_path):
        print(f"Error: File {args.pdf_path} does not exist")
        return
    
    analyzer = CVAnalyzer()
    analyzer.analyze_cv(args.pdf_path)


if __name__ == "__main__":
    main()
