"""
FastAPI backend for CV Chequer application.
Provides REST API endpoints for CV analysis, job matching, and batch processing.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any, Union
import tempfile
import os
import json
import logging
from datetime import datetime

# Import CV Chequer modules
from cv_analyzer import CVAnalyzer
from job_matcher import JobMatcher
from batch_analyzer import BatchCVAnalyzer
from batch_job_matcher import BatchJobMatcher
from config import get_aws_session, validate_aws_services

# Import Pydantic models
from models import (
    CVAnalysisResponse,
    JobMatchRequest,
    JobMatchResponse,
    BatchAnalysisResponse,
    BatchJobMatchResponse,
    ErrorResponse,
    HealthCheckResponse,
    JobDescriptionAnalysisResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CV Chequer API",
    description="A comprehensive CV analysis and job matching API using AWS Textract and Bedrock",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
cv_analyzer = None
job_matcher = None

@app.on_event("startup")
async def startup_event():
    """Initialize AWS services and validate configuration on startup."""
    global cv_analyzer, job_matcher
    try:
        logger.info("Initializing CV Chequer API...")
        
        # Validate AWS services
        validate_aws_services()
        
        # Initialize analyzers
        cv_analyzer = CVAnalyzer()
        job_matcher = JobMatcher()
        
        logger.info("✓ CV Chequer API initialized successfully!")
        
    except Exception as e:
        logger.error(f"✗ Failed to initialize CV Chequer API: {e}")
        raise

@app.get("/", response_model=HealthCheckResponse)
async def root():
    """Root endpoint - API health check."""
    return HealthCheckResponse(
        status="healthy",
        message="CV Chequer API is running",
        version="1.0.0",
        timestamp=datetime.utcnow()
    )

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint."""
    try:
        # Test AWS connection
        session = get_aws_session()
        sts = session.client('sts')
        identity = sts.get_caller_identity()
        
        return HealthCheckResponse(
            status="healthy",
            message="All services operational",
            version="1.0.0",
            timestamp=datetime.utcnow(),
            aws_identity=identity.get('Arn', 'Unknown')
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

@app.post("/analyze-cv", response_model=CVAnalysisResponse)
async def analyze_cv(
    file: UploadFile = File(..., description="PDF file containing the CV to analyze"),
    include_raw_text: bool = Form(False, description="Include extracted raw text in response")
):
    """
    Analyze a single CV from uploaded PDF file.
    
    - **file**: PDF file containing the CV
    - **include_raw_text**: Whether to include the extracted text in the response
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Analyze CV
        logger.info(f"Analyzing CV: {file.filename}")
        analysis_result = cv_analyzer.analyze_cv(temp_file_path)
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        if not analysis_result:
            raise HTTPException(status_code=422, detail="Failed to analyze CV")
        
        # Prepare response
        response_data = {
            "filename": file.filename,
            "analysis": analysis_result,
            "success": True,
            "timestamp": datetime.utcnow()
        }
        
        if include_raw_text and 'raw_text' in analysis_result:
            response_data["raw_text"] = analysis_result.get('raw_text')
        
        return CVAnalysisResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing CV {file.filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/analyze-job-description", response_model=JobDescriptionAnalysisResponse)
async def analyze_job_description(request: JobMatchRequest):
    """
    Analyze a job description to extract requirements.
    
    - **job_description**: The job description text to analyze
    """
    try:
        logger.info("Analyzing job description...")
        job_analysis = job_matcher.analyze_job_description(request.job_description)
        
        if not job_analysis:
            raise HTTPException(status_code=422, detail="Failed to analyze job description")
        
        return JobDescriptionAnalysisResponse(
            analysis=job_analysis,
            success=True,
            timestamp=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing job description: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/match-cv-job", response_model=JobMatchResponse)
async def match_cv_with_job(
    file: UploadFile = File(..., description="PDF file containing the CV"),
    job_description: str = Form(..., description="Job description text")
):
    """
    Match a CV against a job description and provide detailed analysis.
    
    - **file**: PDF file containing the CV
    - **job_description**: Job description text to match against
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Perform job matching
        logger.info(f"Matching CV {file.filename} with job description")
        match_result = job_matcher.compare_cv_with_job(temp_file_path, job_description)
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        if not match_result:
            raise HTTPException(status_code=422, detail="Failed to match CV with job")
        
        return JobMatchResponse(
            filename=file.filename,
            match_analysis=match_result,
            success=True,
            timestamp=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error matching CV {file.filename} with job: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/batch-analyze-cvs", response_model=BatchAnalysisResponse)
async def batch_analyze_cvs(
    files: List[UploadFile] = File(..., description="Multiple PDF files containing CVs"),
    background_tasks: BackgroundTasks = None
):
    """
    Analyze multiple CVs in batch.
    
    - **files**: List of PDF files containing CVs to analyze
    """
    # Validate files
    for file in files:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400, 
                detail=f"File {file.filename} is not a PDF. Only PDF files are supported"
            )
    
    try:
        logger.info(f"Starting batch analysis of {len(files)} CVs")
        batch_analyzer = BatchCVAnalyzer()
        results = []
        
        for file in files:
            try:
                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                    content = await file.read()
                    temp_file.write(content)
                    temp_file_path = temp_file.name
                
                # Analyze CV
                analysis_result = batch_analyzer.analyzer.analyze_cv(temp_file_path)
                
                # Clean up temporary file
                os.unlink(temp_file_path)
                
                if analysis_result:
                    analysis_result['filename'] = file.filename
                    results.append(analysis_result)
                    logger.info(f"✓ Successfully analyzed {file.filename}")
                else:
                    logger.warning(f"✗ Failed to analyze {file.filename}")
                    
            except Exception as e:
                logger.error(f"Error analyzing {file.filename}: {e}")
                continue
        
        if not results:
            raise HTTPException(status_code=422, detail="Failed to analyze any CVs")
        
        return BatchAnalysisResponse(
            total_files=len(files),
            successful_analyses=len(results),
            failed_analyses=len(files) - len(results),
            results=results,
            success=True,
            timestamp=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in batch CV analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/batch-match-cvs-job", response_model=BatchJobMatchResponse)
async def batch_match_cvs_with_job(
    files: List[UploadFile] = File(..., description="Multiple PDF files containing CVs"),
    job_description: str = Form(..., description="Job description text to match against"),
    top_candidates: int = Form(5, description="Number of top candidates to return detailed analysis for")
):
    """
    Match multiple CVs against a job description and rank candidates.
    
    - **files**: List of PDF files containing CVs
    - **job_description**: Job description text to match against
    - **top_candidates**: Number of top candidates to include in detailed results
    """
    # Validate files
    for file in files:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400, 
                detail=f"File {file.filename} is not a PDF. Only PDF files are supported"
            )
    
    try:
        logger.info(f"Starting batch job matching for {len(files)} CVs")
        batch_matcher = BatchJobMatcher()
        results = []
        
        for file in files:
            try:
                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                    content = await file.read()
                    temp_file.write(content)
                    temp_file_path = temp_file.name
                
                # Match CV with job
                match_result = batch_matcher.matcher.compare_cv_with_job(temp_file_path, job_description)
                
                # Clean up temporary file
                os.unlink(temp_file_path)
                
                if match_result:
                    match_result['filename'] = file.filename
                    results.append(match_result)
                    logger.info(f"✓ Successfully matched {file.filename}")
                else:
                    logger.warning(f"✗ Failed to match {file.filename}")
                    
            except Exception as e:
                logger.error(f"Error matching {file.filename}: {e}")
                continue
        
        if not results:
            raise HTTPException(status_code=422, detail="Failed to match any CVs with job description")
        
        # Sort by overall score
        sorted_results = sorted(results, key=lambda x: x.get('overall_score', 0), reverse=True)
        top_results = sorted_results[:top_candidates]
        
        return BatchJobMatchResponse(
            total_files=len(files),
            successful_matches=len(results),
            failed_matches=len(files) - len(results),
            top_candidates=top_results,
            all_candidates_summary=[{
                'filename': r.get('filename'),
                'candidate_name': r.get('candidate_name'),
                'overall_score': r.get('overall_score'),
                'technology_score': r.get('technology_match', {}).get('score', 0),
                'soft_skills_score': r.get('soft_skills_match', {}).get('score', 0),
                'experience_score': r.get('experience_match', {}).get('score', 0)
            } for r in sorted_results],
            success=True,
            timestamp=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in batch job matching: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(
            error="Not Found",
            message="The requested endpoint was not found",
            timestamp=datetime.utcnow()
        ).dict()
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal Server Error",
            message="An unexpected error occurred",
            timestamp=datetime.utcnow()
        ).dict()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
