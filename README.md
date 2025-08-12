# CV Chequer - AI-Powered CV Analysis & Job Matching

A comprehensive Python application with both CLI tools and REST API that uses AWS Textract to extract text from CV PDFs and AWS Bedrock to analyze and categorize the information. Now includes a modern FastAPI backend for web integration.

## Features

- Extract text from PDF CVs using AWS Textract (with fallback methods)
- Analyze CV content using AWS Bedrock (Claude)
- Categorize technologies into:
  - Programming Languages
  - Cloud Services (AWS, Azure, GCP, others)
  - Databases
  - DevOps tools
  - Other technologies
- **Soft Skills Analysis** - Extract and analyze soft skills with evidence:
  - Leadership & Management
  - Communication & Collaboration
  - Problem Solving & Analytical Thinking
  - Adaptability & Learning
  - Time Management & Organization
  - Creativity & Innovation
  - Interpersonal Skills
  - Others
- **Job Description Matching** - Compare CVs against job requirements:
  - Percentage match scoring (overall, technology, soft skills, experience)
  - Detailed gap analysis showing missing skills/technologies
  - Importance-weighted scoring based on job requirements
  - Batch candidate ranking and comparison
- Probability analysis for authenticity of mentioned technologies
- Confidence analysis for soft skills with supporting evidence
- Command-line table display of results
- Batch processing with comparison tables
- **FastAPI REST API** - Modern web API with:
  - Interactive API documentation (Swagger UI & ReDoc)
  - File upload endpoints for CV analysis
  - Job description analysis and matching
  - Batch processing endpoints
  - Comprehensive error handling and validation
  - CORS support for web integration

## Setup

### Quick Setup (Recommended)

```bash
# Run the automated installation script
python install_requirements.py
```

### Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure AWS credentials (choose one method):

   **Method A - Environment Variables:**
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_REGION=us-east-1
   ```

   **Method B - .env file:**
   Create a `.env` file in the project directory:
   ```
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_REGION=us-east-1
   AWS_BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
   ```

   **Method C - AWS CLI:**
   ```bash
   aws configure
   ```

3. **Verify setup:**
```bash
python setup_check.py
```

## AWS Requirements

- AWS account with active credentials
- Enabled services: Textract, Bedrock
- Required permissions:
  - `textract:DetectDocumentText`
  - `bedrock:InvokeModel`
  - `bedrock:ListFoundationModels`
- Bedrock model access enabled (Claude models) in AWS Console

## Usage

### FastAPI REST API

#### Starting the API Server

```bash
# Start the API server
python scripts/start_api.py

# Or using uvicorn directly from project root
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative Documentation (ReDoc)**: http://localhost:8000/redoc

#### API Endpoints

**Health Check**
```bash
GET /health
# Returns API status and AWS connectivity
```

**CV Analysis**
```bash
POST /analyze-cv
# Upload a PDF file for CV analysis
# Returns: candidate info, technologies, soft skills with confidence scores
```

**Job Description Analysis**
```bash
POST /analyze-job-description
# Analyze job requirements from description text
# Returns: extracted requirements with importance levels
```

**CV-Job Matching**
```bash
POST /match-cv-job
# Match a CV against a job description
# Returns: detailed match analysis with scores and gaps
```

**Batch CV Analysis**
```bash
POST /batch-analyze-cvs
# Analyze multiple CVs simultaneously
# Returns: consolidated analysis results
```

**Batch CV-Job Matching**
```bash
POST /batch-match-cvs-job
# Match multiple CVs against a job description
# Returns: ranked candidates with detailed analysis
```

#### Testing the API

```bash
# Run the comprehensive API test suite
python examples/api_example.py

# Or test individual endpoints using curl:

# Health check
curl -X GET "http://localhost:8000/health"

# CV analysis
curl -X POST "http://localhost:8000/analyze-cv" \
  -F "file=@path/to/cv.pdf" \
  -F "include_raw_text=false"

# Job description analysis
curl -X POST "http://localhost:8000/analyze-job-description" \
  -H "Content-Type: application/json" \
  -d '{"job_description": "Senior Developer with Python and AWS experience..."}'
```

### Command Line Interface (CLI)

#### CV Analysis Only

Analyze a single CV:
```bash
python src/cli/analyze_cv.py "data/CV_FullStack/EPAM/CV Brayan Urbina Gomez.pdf"
```

Batch analyze multiple CVs:
```bash
python src/cli/batch_analyze.py data/CV_FullStack/EPAM
```

#### Job Description Matching

Compare single CV with job description:
```bash
# Using job description file
python src/cli/match_job.py "data/CV_FullStack/EPAM/CV Brayan Urbina Gomez.pdf" --job-file examples/example_job_description.txt

# Using direct text input
python src/cli/match_job.py "data/CV_FullStack/EPAM/CV Brayan Urbina Gomez.pdf" --job-text "We are looking for a Senior Developer with React and AWS experience..."

# Interactive mode (enter job description when prompted)
python src/cli/match_job.py "data/CV_FullStack/EPAM/CV Brayan Urbina Gomez.pdf"
```

#### Interactive Examples
```bash
python examples/example_usage.py
```

## Troubleshooting

If you see "UnrecognizedClientException" or credential errors:

1. **Run the setup verification script:**
   ```bash
   python src/utils/setup_check.py
   ```

2. **Check your AWS credentials are valid:**
   ```bash
   aws sts get-caller-identity
   ```

3. **Ensure Bedrock model access is enabled:**
   - Go to AWS Console > Bedrock > Model access
   - Enable Claude 3 Sonnet model

4. **Verify region configuration** (Bedrock availability varies by region)

## Requirements

- AWS account with Textract and Bedrock access
- Python 3.8+
- AWS credentials configured
- For API: FastAPI, Uvicorn, and Python-multipart (installed via requirements.txt)

## Output

The tool will display formatted tables with:
- **Basic Information**: Candidate name and years of experience
- **Technologies** categorized by type with authenticity probability percentages
- **Soft Skills** organized by categories with:
  - Confidence percentage (0-100%)
  - Supporting evidence from the CV
  - Categories: Leadership, Communication, Problem Solving, Adaptability, etc.
- **Batch Analysis**: Comparison tables across multiple CVs showing technology and soft skill distributions

### API Response Examples:

**CV Analysis Response:**
```json
{
  "success": true,
  "timestamp": "2024-01-15T10:30:00Z",
  "filename": "john_doe_cv.pdf",
  "analysis": {
    "name": "John Doe",
    "years_of_experience": "5 years",
    "technologies": {
      "programming_languages": [
        {"name": "Python", "probability": 95},
        {"name": "JavaScript", "probability": 88}
      ],
      "cloud_services": {
        "aws": [
          {"name": "EC2", "probability": 90},
          {"name": "S3", "probability": 85}
        ]
      },
      "databases": [
        {"name": "PostgreSQL", "probability": 92}
      ]
    },
    "soft_skills": {
      "leadership_management": [
        {
          "skill": "Team Leadership",
          "confidence": 85,
          "evidence": "Led team of 5 developers"
        }
      ]
    }
  }
}
```

**Job Match Response:**
```json
{
  "success": true,
  "timestamp": "2024-01-15T10:35:00Z",
  "filename": "john_doe_cv.pdf",
  "match_analysis": {
    "overall_score": 82.5,
    "candidate_name": "John Doe",
    "job_title": "Senior Python Developer",
    "technology_match": {
      "score": 85.0,
      "matched_count": 8,
      "total_requirements": 10
    },
    "soft_skills_match": {
      "score": 78.0,
      "matched_count": 6,
      "total_requirements": 8
    },
    "experience_match": {
      "score": 100.0,
      "meets_requirement": true
    }
  }
}
```

### CLI Output Sections:
- **CV Analysis**: Programming Languages, Cloud Services, Databases, DevOps Tools
- **Soft Skills**: Leadership & Management, Communication & Collaboration, Problem Solving
- **Job Matching**: Overall match percentage, technology gaps, skill gaps, candidate ranking

### Job Matching Output Example:
```
================================================================================
JOB MATCH ANALYSIS
================================================================================
Candidate: John Doe
Position: Senior Full Stack Developer
Overall Match Score: 78.5%

┌─────────────────────┬────────────┬─────────┐
│ Category            │ Score      │ Weight  │
├─────────────────────┼────────────┼─────────┤
│ Technology Match    │ 85.0%      │ 50%     │
│ Soft Skills Match   │ 70.0%      │ 30%     │
│ Experience Match    │ 100.0%     │ 20%     │
│ OVERALL SCORE       │ 78.5%      │ 100%    │
└─────────────────────┴────────────┴─────────┘
```
