"""
Pydantic models for FastAPI CV Chequer application.
Defines request and response schemas for all API endpoints.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

# Base models
class BaseResponse(BaseModel):
    """Base response model with common fields."""
    success: bool = Field(..., description="Whether the operation was successful")
    timestamp: datetime = Field(..., description="Timestamp of the response")

class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    timestamp: datetime = Field(..., description="Timestamp of the error")

# Technology models
class Technology(BaseModel):
    """Technology item with probability/confidence score."""
    name: str = Field(..., description="Technology name")
    probability: int = Field(..., ge=0, le=100, description="Authenticity probability (0-100)")

class CloudServices(BaseModel):
    """Cloud services organized by provider."""
    aws: List[Technology] = Field(default=[], description="AWS services")
    azure: List[Technology] = Field(default=[], description="Azure services")
    gcp: List[Technology] = Field(default=[], description="Google Cloud services")
    others: List[Technology] = Field(default=[], description="Other cloud services")

class Technologies(BaseModel):
    """Complete technology analysis."""
    programming_languages: List[Technology] = Field(default=[], description="Programming languages")
    cloud_services: CloudServices = Field(default=CloudServices(), description="Cloud services by provider")
    databases: List[Technology] = Field(default=[], description="Database technologies")
    devops: List[Technology] = Field(default=[], description="DevOps tools")
    others: List[Technology] = Field(default=[], description="Other technologies")

# Soft skills models
class SoftSkill(BaseModel):
    """Soft skill with confidence and evidence."""
    skill: str = Field(..., description="Skill name")
    confidence: int = Field(..., ge=0, le=100, description="Confidence level (0-100)")
    evidence: str = Field(..., description="Supporting evidence from CV")

class SoftSkills(BaseModel):
    """Complete soft skills analysis."""
    leadership_management: List[SoftSkill] = Field(default=[], description="Leadership and management skills")
    communication_collaboration: List[SoftSkill] = Field(default=[], description="Communication and collaboration skills")
    problem_solving_analytical: List[SoftSkill] = Field(default=[], description="Problem solving and analytical skills")
    adaptability_learning: List[SoftSkill] = Field(default=[], description="Adaptability and learning skills")
    time_management_organization: List[SoftSkill] = Field(default=[], description="Time management and organization skills")
    creativity_innovation: List[SoftSkill] = Field(default=[], description="Creativity and innovation skills")
    interpersonal: List[SoftSkill] = Field(default=[], description="Interpersonal skills")
    others: List[SoftSkill] = Field(default=[], description="Other soft skills")

# CV Analysis models
class CVAnalysis(BaseModel):
    """Complete CV analysis result."""
    name: str = Field(..., description="Candidate name")
    years_of_experience: str = Field(..., description="Years of professional experience")
    technologies: Technologies = Field(..., description="Technology analysis")
    soft_skills: SoftSkills = Field(..., description="Soft skills analysis")

class CVAnalysisResponse(BaseResponse):
    """Response for CV analysis endpoint."""
    filename: str = Field(..., description="Name of the analyzed file")
    analysis: CVAnalysis = Field(..., description="CV analysis results")
    raw_text: Optional[str] = Field(None, description="Extracted raw text (if requested)")

# Job requirements models
class RequiredTechnology(BaseModel):
    """Required technology with importance level."""
    name: str = Field(..., description="Technology name")
    importance: int = Field(..., ge=1, le=5, description="Importance level (1-5)")
    required: bool = Field(..., description="Whether this technology is required")

class RequiredCloudServices(BaseModel):
    """Required cloud services by provider."""
    aws: List[RequiredTechnology] = Field(default=[], description="AWS services")
    azure: List[RequiredTechnology] = Field(default=[], description="Azure services")
    gcp: List[RequiredTechnology] = Field(default=[], description="Google Cloud services")
    others: List[RequiredTechnology] = Field(default=[], description="Other cloud services")

class RequiredTechnologies(BaseModel):
    """Complete required technologies."""
    programming_languages: List[RequiredTechnology] = Field(default=[], description="Required programming languages")
    cloud_services: RequiredCloudServices = Field(default=RequiredCloudServices(), description="Required cloud services")
    databases: List[RequiredTechnology] = Field(default=[], description="Required databases")
    devops: List[RequiredTechnology] = Field(default=[], description="Required DevOps tools")
    others: List[RequiredTechnology] = Field(default=[], description="Other required technologies")

class RequiredSoftSkill(BaseModel):
    """Required soft skill with importance level."""
    skill: str = Field(..., description="Skill name")
    importance: int = Field(..., ge=1, le=5, description="Importance level (1-5)")
    required: bool = Field(..., description="Whether this skill is required")

class RequiredSoftSkills(BaseModel):
    """Complete required soft skills."""
    leadership_management: List[RequiredSoftSkill] = Field(default=[], description="Leadership and management requirements")
    communication_collaboration: List[RequiredSoftSkill] = Field(default=[], description="Communication and collaboration requirements")
    problem_solving_analytical: List[RequiredSoftSkill] = Field(default=[], description="Problem solving requirements")
    adaptability_learning: List[RequiredSoftSkill] = Field(default=[], description="Adaptability and learning requirements")
    time_management_organization: List[RequiredSoftSkill] = Field(default=[], description="Time management requirements")
    creativity_innovation: List[RequiredSoftSkill] = Field(default=[], description="Creativity and innovation requirements")
    interpersonal: List[RequiredSoftSkill] = Field(default=[], description="Interpersonal skills requirements")
    others: List[RequiredSoftSkill] = Field(default=[], description="Other required soft skills")

class JobAnalysis(BaseModel):
    """Job description analysis result."""
    job_title: str = Field(..., description="Job title")
    seniority_level: str = Field(..., description="Seniority level (Junior/Mid/Senior/Lead)")
    experience_required: str = Field(..., description="Required years of experience")
    required_technologies: RequiredTechnologies = Field(..., description="Required technologies")
    required_soft_skills: RequiredSoftSkills = Field(..., description="Required soft skills")
    key_responsibilities: List[str] = Field(default=[], description="Key job responsibilities")
    nice_to_have: List[str] = Field(default=[], description="Nice-to-have qualifications")

# Job matching models
class MatchedItem(BaseModel):
    """Matched technology or skill item."""
    name: str = Field(..., description="Item name")
    category: str = Field(..., description="Category")
    importance: int = Field(..., ge=1, le=5, description="Job importance level")
    cv_probability: Optional[int] = Field(None, ge=0, le=100, description="CV authenticity/confidence score")
    cv_confidence: Optional[int] = Field(None, ge=0, le=100, description="CV confidence score (for skills)")

class MissingItem(BaseModel):
    """Missing technology or skill item."""
    name: str = Field(..., description="Item name")
    category: str = Field(..., description="Category")
    importance: int = Field(..., ge=1, le=5, description="Job importance level")
    required: bool = Field(..., description="Whether this item is required")

class MatchAnalysis(BaseModel):
    """Match analysis for a category (technology or soft skills)."""
    matched: List[MatchedItem] = Field(..., description="Matched items")
    missing: List[MissingItem] = Field(..., description="Missing items")
    score: float = Field(..., ge=0, le=100, description="Match score percentage")
    matched_count: int = Field(..., ge=0, description="Number of matched items")
    total_requirements: int = Field(..., ge=0, description="Total number of requirements")

class ExperienceMatch(BaseModel):
    """Experience match analysis."""
    cv_experience: str = Field(..., description="Candidate's experience")
    required_experience: str = Field(..., description="Required experience")
    score: float = Field(..., ge=0, le=100, description="Experience match score")
    meets_requirement: bool = Field(..., description="Whether candidate meets experience requirement")

class JobMatchAnalysis(BaseModel):
    """Complete job match analysis."""
    overall_score: float = Field(..., ge=0, le=100, description="Overall match score")
    technology_match: MatchAnalysis = Field(..., description="Technology match analysis")
    soft_skills_match: MatchAnalysis = Field(..., description="Soft skills match analysis")
    experience_match: ExperienceMatch = Field(..., description="Experience match analysis")
    candidate_name: str = Field(..., description="Candidate name")
    job_title: str = Field(..., description="Job title")

# Request models
class JobMatchRequest(BaseModel):
    """Request for job description analysis."""
    job_description: str = Field(..., min_length=10, description="Job description text to analyze")
    
    @validator('job_description')
    def validate_job_description(cls, v):
        if not v.strip():
            raise ValueError('Job description cannot be empty')
        return v.strip()

# Response models
class JobDescriptionAnalysisResponse(BaseResponse):
    """Response for job description analysis."""
    analysis: JobAnalysis = Field(..., description="Job analysis results")

class JobMatchResponse(BaseResponse):
    """Response for single CV job matching."""
    filename: str = Field(..., description="CV filename")
    match_analysis: JobMatchAnalysis = Field(..., description="Job match analysis")

class BatchAnalysisResponse(BaseResponse):
    """Response for batch CV analysis."""
    total_files: int = Field(..., ge=0, description="Total number of files processed")
    successful_analyses: int = Field(..., ge=0, description="Number of successful analyses")
    failed_analyses: int = Field(..., ge=0, description="Number of failed analyses")
    results: List[CVAnalysis] = Field(..., description="Analysis results for all CVs")

class CandidateSummary(BaseModel):
    """Summary of a candidate for batch job matching."""
    filename: str = Field(..., description="CV filename")
    candidate_name: str = Field(..., description="Candidate name")
    overall_score: float = Field(..., ge=0, le=100, description="Overall match score")
    technology_score: float = Field(..., ge=0, le=100, description="Technology match score")
    soft_skills_score: float = Field(..., ge=0, le=100, description="Soft skills match score")
    experience_score: float = Field(..., ge=0, le=100, description="Experience match score")

class BatchJobMatchResponse(BaseResponse):
    """Response for batch job matching."""
    total_files: int = Field(..., ge=0, description="Total number of files processed")
    successful_matches: int = Field(..., ge=0, description="Number of successful matches")
    failed_matches: int = Field(..., ge=0, description="Number of failed matches")
    top_candidates: List[JobMatchAnalysis] = Field(..., description="Detailed analysis of top candidates")
    all_candidates_summary: List[CandidateSummary] = Field(..., description="Summary of all candidates ranked by score")

class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Status message")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(..., description="Response timestamp")
    aws_identity: Optional[str] = Field(None, description="AWS identity (if available)")

# Additional utility models
class FileUploadInfo(BaseModel):
    """File upload information."""
    filename: str = Field(..., description="Original filename")
    size: int = Field(..., ge=0, description="File size in bytes")
    content_type: str = Field(..., description="File content type")

class ProcessingStatus(str, Enum):
    """Processing status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class BatchJobStatus(BaseModel):
    """Batch job status information."""
    job_id: str = Field(..., description="Unique job identifier")
    status: ProcessingStatus = Field(..., description="Current job status")
    total_files: int = Field(..., ge=0, description="Total number of files in the job")
    processed_files: int = Field(..., ge=0, description="Number of files processed")
    created_at: datetime = Field(..., description="Job creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    estimated_completion: Optional[datetime] = Field(None, description="Estimated completion time")
