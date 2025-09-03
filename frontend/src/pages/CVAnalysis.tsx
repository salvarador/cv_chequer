import React, { useState } from 'react';
import { FileText, Download, Eye, EyeOff } from 'lucide-react';
import FileUpload from '../components/UI/FileUpload';
import LoadingSpinner from '../components/UI/LoadingSpinner';
import TechnologyDisplay from '../components/CVAnalysis/TechnologyDisplay';
import SoftSkillsDisplay from '../components/CVAnalysis/SoftSkillsDisplay';
import { apiService, type CVAnalysisResponse } from '../services/api';
import { formatDate } from '../utils/helpers';

const CVAnalysis: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<CVAnalysisResponse | null>(null);
  const [includeRawText, setIncludeRawText] = useState(false);
  const [showRawText, setShowRawText] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileSelected = (files: File[]) => {
    setSelectedFile(files[0] || null);
    setAnalysisResult(null);
    setError(null);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('Please select a CV file to analyze');
      return;
    }

    setIsAnalyzing(true);
    setError(null);

    try {
      const result = await apiService.analyzeCV(selectedFile, includeRawText);
      setAnalysisResult(result);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze CV. Please try again.');
      console.error('CV Analysis error:', err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const downloadReport = () => {
    if (!analysisResult) return;

    const reportData = {
      filename: analysisResult.filename,
      timestamp: analysisResult.timestamp,
      candidate: {
        name: analysisResult.analysis.name,
        experience: analysisResult.analysis.years_of_experience,
      },
      technologies: analysisResult.analysis.technologies,
      soft_skills: analysisResult.analysis.soft_skills,
    };

    const dataStr = JSON.stringify(reportData, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `cv-analysis-${analysisResult.analysis.name.replace(/\s+/g, '-').toLowerCase()}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 flex items-center">
              <FileText className="h-7 w-7 text-primary-600 mr-3" />
              CV Analysis
            </h1>
            <p className="mt-1 text-sm text-gray-600">
              Upload a CV in PDF format to extract technologies, skills, and experience using AI analysis
            </p>
          </div>
          {analysisResult && (
            <button
              onClick={downloadReport}
              className="btn-secondary flex items-center space-x-2"
            >
              <Download className="h-4 w-4" />
              <span>Download Report</span>
            </button>
          )}
        </div>
      </div>

      {/* Upload Section */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Upload CV</h2>
        
        <FileUpload
          onFilesSelected={handleFileSelected}
          multiple={false}
          maxFiles={1}
          disabled={isAnalyzing}
        />

        {selectedFile && (
          <div className="mt-4 space-y-4">
            <div className="flex items-center space-x-4">
              <div className="flex items-center">
                <input
                  id="include-raw-text"
                  type="checkbox"
                  checked={includeRawText}
                  onChange={(e) => setIncludeRawText(e.target.checked)}
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label htmlFor="include-raw-text" className="ml-2 text-sm text-gray-700">
                  Include extracted text in results
                </label>
              </div>
            </div>

            <button
              onClick={handleAnalyze}
              disabled={isAnalyzing}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isAnalyzing ? (
                <div className="flex items-center space-x-2">
                  <LoadingSpinner size="sm" />
                  <span>Analyzing CV...</span>
                </div>
              ) : (
                'Analyze CV'
              )}
            </button>
          </div>
        )}

        {error && (
          <div className="mt-4 bg-red-50 border border-red-200 rounded-md p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Analysis Error</h3>
                <div className="mt-2 text-sm text-red-700">
                  <p>{error}</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Results Section */}
      {analysisResult && (
        <div className="space-y-6">
          {/* Basic Information */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Candidate Information</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <dt className="text-sm font-medium text-gray-500">Name</dt>
                <dd className="mt-1 text-lg font-semibold text-gray-900">
                  {analysisResult.analysis.name}
                </dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Experience</dt>
                <dd className="mt-1 text-lg font-semibold text-gray-900">
                  {analysisResult.analysis.years_of_experience}
                </dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Analyzed</dt>
                <dd className="mt-1 text-lg font-semibold text-gray-900">
                  {formatDate(analysisResult.timestamp)}
                </dd>
              </div>
            </div>
          </div>

          {/* Technologies */}
          <TechnologyDisplay technologies={analysisResult.analysis.technologies} />

          {/* Soft Skills */}
          <SoftSkillsDisplay softSkills={analysisResult.analysis.soft_skills} />

          {/* Raw Text */}
          {analysisResult.raw_text && (
            <div className="bg-white shadow rounded-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-gray-900">Extracted Text</h2>
                <button
                  onClick={() => setShowRawText(!showRawText)}
                  className="btn-secondary flex items-center space-x-2"
                >
                  {showRawText ? (
                    <>
                      <EyeOff className="h-4 w-4" />
                      <span>Hide Text</span>
                    </>
                  ) : (
                    <>
                      <Eye className="h-4 w-4" />
                      <span>Show Text</span>
                    </>
                  )}
                </button>
              </div>
              
              {showRawText && (
                <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
                  <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                    {analysisResult.raw_text}
                  </pre>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default CVAnalysis;
