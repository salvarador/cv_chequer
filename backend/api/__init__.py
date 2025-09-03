"""
FastAPI REST API Module

This package contains the REST API components:
- main: FastAPI application with all endpoints
- models: Pydantic models for request/response validation
"""

from .main import app
from .models import *

__all__ = ['app']
