
# Copilot Instructions for CV Chequer

## Project Architecture
CV Chequer is an AI-powered CV analysis and job matching platform with:
- **Python FastAPI backend** (`backend/api/main.py`): REST API exposing all CLI functionality, with endpoints for CV analysis, job extraction, matching, and batch operations.
- **CLI tools** (`backend/cli/`): Direct access to analysis and matching logic for batch/single operations.
- **React frontend** (`frontend/src/`): Modern UI for CV upload, analysis, and job matching, communicating via REST API.
- **AWS Integration**: Textract (PDF extraction), Bedrock Claude (AI analysis/matching).

### Data Flow
1. **CV PDFs** (`data/`, `uploaded_cvs/`, or upload) → Textract → Raw text
2. **Raw text** → Bedrock Claude → Structured analysis (technologies, soft skills, experience)
3. **Job descriptions** (text/file) → Bedrock Claude → Requirements extraction
4. **Matching logic**: Compares CV analysis with job requirements, scores, and ranks candidates
5. **Results** → API/CLI/Frontend → User

## Developer Workflows
- **Setup**: `python scripts/install_requirements.py` (validates Python version, installs dependencies, checks AWS credentials)
- **Start API**: `python scripts/start_api.py` (configurable, auto-reload, CORS enabled)
- **Run CLI**: e.g. `python backend/cli/analyze_cv.py <cv_path>`, `python backend/cli/match_job.py <cv_path> --job-file <job_desc.txt>`
- **Frontend dev**: `python start_frontend.py` (wrapper for Vite dev server)
- **Test API**: `python examples/api_example.py` (covers all endpoints, uses sample data)
- **Health check**: `GET /health` (verifies AWS connectivity)

## Project-Specific Conventions
- **Technologies**: Categorized as programming languages, cloud, databases, DevOps, other (see `backend/core/cv_analyzer.py`)
- **Soft skills**: Extracted with confidence scores and supporting evidence
- **API responses**: Always include `success`, `timestamp`, and detailed analysis/match objects
- **Batch operations**: Supported in both CLI and API (`/batch-analyze-cvs`, `/batch-match-cvs-job`)
- **Frontend API calls**: Use `backend/services/api.ts` for backend communication
- **Environment config**: `.env` for both backend and frontend; see README for required variables

## Integration Points & External Dependencies
- **AWS Textract**: PDF extraction (fallbacks if unavailable)
- **AWS Bedrock Claude**: All AI analysis and matching
- **CORS**: Enabled for frontend-backend communication
- **Testing**: Example API tests in `examples/api_example.py`; CLI usage in `examples/example_usage.py`

## Key Files & Directories
- `backend/api/main.py`: FastAPI app and endpoints
- `backend/core/`: Core analysis and matching logic
- `backend/cli/`: CLI entry points
- `frontend/scr/`: React app code
- `scripts/`: Setup and startup scripts
- `examples/`: Usage and API examples
- `data/`: Sample CVs

## For AI Agents
- Use provided CLI/API/Frontend entry points for analysis and matching
- Follow technology and soft skill categorization patterns in core logic
- Reference the README for setup, environment, and workflow details
- Use batch endpoints and CLI tools for multi-CV operations
- Prefer existing API/CLI for new features unless architectural changes are required

---
**Tip:** For any new feature, first check for an existing CLI or API entry point before adding new logic. Always maintain consistent data formats and error handling as defined in Pydantic models.
