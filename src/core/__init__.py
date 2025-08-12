"""
Core CV Analysis and Job Matching Modules

This package contains the main analysis engines:
- cv_analyzer: PDF text extraction and CV analysis
- job_matcher: Job description analysis and CV-job matching
- batch_analyzer: Batch CV processing and comparison
- batch_job_matcher: Batch CV-job matching and ranking
- config: AWS configuration and authentication
"""

from .cv_analyzer import CVAnalyzer
from .job_matcher import JobMatcher
from .batch_analyzer import BatchCVAnalyzer
from .batch_job_matcher import BatchJobMatcher
from .config import get_aws_session, BEDROCK_MODEL_ID

__all__ = [
    'CVAnalyzer',
    'JobMatcher', 
    'BatchCVAnalyzer',
    'BatchJobMatcher',
    'get_aws_session',
    'BEDROCK_MODEL_ID'
]
