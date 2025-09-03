import axios, { type AxiosResponse } from 'axios';

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Type definitions for API responses
export interface CVAnalysisResult {
  name: string;
  years_of_experience: string;
  technologies: {
    programming_languages: Array<{ name: string; probability: number }>;
    cloud_services: {
      aws?: Array<{ name: string; probability: number }>;
      azure?: Array<{ name: string; probability: number }>;
      gcp?: Array<{ name: string; probability: number }>;
      others?: Array<{ name: string; probability: number }>;
    };
    databases: Array<{ name: string; probability: number }>;
    devops_tools: Array<{ name: string; probability: number }>;
    other_technologies: Array<{ name: string; probability: number }>;
  };
  soft_skills: {
    leadership_management?: Array<{
      skill: string;
      confidence: number;
      evidence: string;
    }>;
    communication_collaboration?: Array<{
      skill: string;
      confidence: number;
      evidence: string;
    }>;
    problem_solving_analytical?: Array<{
      skill: string;
      confidence: number;
      evidence: string;
    }>;
    adaptability_learning?: Array<{
      skill: string;
      confidence: number;
      evidence: string;
    }>;
    time_management_organization?: Array<{
      skill: string;
      confidence: number;
      evidence: string;
    }>;
    creativity_innovation?: Array<{
      skill: string;
      confidence: number;
      evidence: string;
    }>;
    interpersonal_skills?: Array<{
      skill: string;
      confidence: number;
      evidence: string;
    }>;
    others?: Array<{
      skill: string;
      confidence: number;
      evidence: string;
    }>;
  };
  raw_text?: string;
}

export interface CVAnalysisResponse {
  success: boolean;
  timestamp: string;
  filename: string;
  analysis: CVAnalysisResult;
  raw_text?: string;
}

export interface JobRequirements {
  required_technologies: {
    programming_languages: Array<{ name: string; importance: string }>;
    cloud_services: {
      aws?: Array<{ name: string; importance: string }>;
      azure?: Array<{ name: string; importance: string }>;
      gcp?: Array<{ name: string; importance: string }>;
      others?: Array<{ name: string; importance: string }>;
    };
    databases: Array<{ name: string; importance: string }>;
    devops_tools: Array<{ name: string; importance: string }>;
    other_technologies: Array<{ name: string; importance: string }>;
  };
  required_soft_skills: {
    leadership_management?: Array<{ skill: string; importance: string }>;
    communication_collaboration?: Array<{ skill: string; importance: string }>;
    problem_solving_analytical?: Array<{ skill: string; importance: string }>;
    adaptability_learning?: Array<{ skill: string; importance: string }>;
    time_management_organization?: Array<{ skill: string; importance: string }>;
    creativity_innovation?: Array<{ skill: string; importance: string }>;
    interpersonal_skills?: Array<{ skill: string; importance: string }>;
    others?: Array<{ skill: string; importance: string }>;
  };
  minimum_experience: string;
  job_title: string;
  job_level: string;
}

export interface JobDescriptionAnalysisResponse {
  success: boolean;
  timestamp: string;
  analysis: JobRequirements;
}

export interface MatchAnalysis {
  overall_score: number;
  candidate_name: string;
  job_title: string;
  technology_match: {
    score: number;
    matched_count: number;
    total_requirements: number;
    matched_technologies: Array<{ name: string; category: string }>;
    missing_technologies: Array<{ name: string; category: string; importance: string }>;
  };
  soft_skills_match: {
    score: number;
    matched_count: number;
    total_requirements: number;
    matched_skills: Array<{ skill: string; category: string }>;
    missing_skills: Array<{ skill: string; category: string; importance: string }>;
  };
  experience_match: {
    score: number;
    meets_requirement: boolean;
    candidate_experience: string;
    required_experience: string;
  };
}

export interface JobMatchResponse {
  success: boolean;
  timestamp: string;
  filename: string;
  match_analysis: MatchAnalysis;
}

export interface BatchAnalysisResponse {
  success: boolean;
  timestamp: string;
  total_files: number;
  successful_analyses: number;
  failed_analyses: number;
  results: Array<CVAnalysisResult & { filename: string }>;
}

export interface CandidateSummary {
  filename: string;
  candidate_name: string;
  overall_score: number;
  technology_score: number;
  soft_skills_score: number;
  experience_score: number;
}

export interface BatchJobMatchResponse {
  success: boolean;
  timestamp: string;
  total_files: number;
  successful_matches: number;
  failed_matches: number;
  top_candidates: Array<MatchAnalysis & { filename: string }>;
  all_candidates_summary: CandidateSummary[];
}

export interface HealthCheckResponse {
  status: string;
  message: string;
  version: string;
  timestamp: string;
  aws_identity?: string;
}

// API Functions
export const apiService = {
  // Health check
  healthCheck: async (): Promise<HealthCheckResponse> => {
    const response: AxiosResponse<HealthCheckResponse> = await api.get('/health');
    return response.data;
  },

  // CV Analysis
  analyzeCV: async (file: File, includeRawText: boolean = false): Promise<CVAnalysisResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('include_raw_text', includeRawText.toString());

    const response: AxiosResponse<CVAnalysisResponse> = await api.post('/analyze-cv', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Job Description Analysis
  analyzeJobDescription: async (jobDescription: string): Promise<JobDescriptionAnalysisResponse> => {
    const response: AxiosResponse<JobDescriptionAnalysisResponse> = await api.post('/analyze-job-description', {
      job_description: jobDescription,
    });
    return response.data;
  },

  // CV-Job Matching
  matchCVWithJob: async (file: File, jobDescription: string): Promise<JobMatchResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('job_description', jobDescription);

    const response: AxiosResponse<JobMatchResponse> = await api.post('/match-cv-job', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Batch CV Analysis
  batchAnalyzeCVs: async (files: File[]): Promise<BatchAnalysisResponse> => {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });

    const response: AxiosResponse<BatchAnalysisResponse> = await api.post('/batch-analyze-cvs', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Batch CV-Job Matching
  batchMatchCVsWithJob: async (
    files: File[],
    jobDescription: string,
    topCandidates: number = 5
  ): Promise<BatchJobMatchResponse> => {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });
    formData.append('job_description', jobDescription);
    formData.append('top_candidates', topCandidates.toString());

    const response: AxiosResponse<BatchJobMatchResponse> = await api.post('/batch-match-cvs-job', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

export default apiService;
