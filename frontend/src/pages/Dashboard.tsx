import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  FileText, 
  Search, 
  BarChart3, 
  Users, 
  Upload,
  FileSearch,
  Activity,
  TrendingUp,
  Clock,
  CheckCircle
} from 'lucide-react';
import { apiService } from '../services/api';

interface DashboardStats {
  apiStatus: 'connected' | 'disconnected' | 'checking';
  lastCheck: string;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats>({
    apiStatus: 'checking',
    lastCheck: new Date().toISOString()
  });

  useEffect(() => {
    const checkApiStatus = async () => {
      try {
        await apiService.healthCheck();
        setStats(prev => ({
          ...prev,
          apiStatus: 'connected',
          lastCheck: new Date().toISOString()
        }));
      } catch (error) {
        setStats(prev => ({
          ...prev,
          apiStatus: 'disconnected',
          lastCheck: new Date().toISOString()
        }));
      }
    };

    checkApiStatus();
    const interval = setInterval(checkApiStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const features = [
    {
      name: 'CV Analysis',
      description: 'Analyze single CV for technologies and soft skills',
      icon: FileText,
      href: '/cv-analysis',
      color: 'bg-blue-500',
      stats: 'Extract skills & experience'
    },
    {
      name: 'Job Matching',
      description: 'Match CV against job requirements',
      icon: FileSearch,
      href: '/job-matching',
      color: 'bg-green-500',
      stats: 'Get match scores'
    },
    {
      name: 'Batch Analysis',
      description: 'Analyze multiple CVs simultaneously',
      icon: Upload,
      href: '/batch-analysis',
      color: 'bg-purple-500',
      stats: 'Process multiple files'
    },
    {
      name: 'Batch Matching',
      description: 'Rank candidates against job description',
      icon: Users,
      href: '/batch-matching',
      color: 'bg-orange-500',
      stats: 'Rank candidates'
    },
    {
      name: 'Job Analysis',
      description: 'Analyze job descriptions for requirements',
      icon: Search,
      href: '/job-analysis',
      color: 'bg-indigo-500',
      stats: 'Extract requirements'
    },
    {
      name: 'Reports',
      description: 'View analysis reports and statistics',
      icon: BarChart3,
      href: '/reports',
      color: 'bg-pink-500',
      stats: 'View insights'
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Welcome to CV Chequer</h1>
            <p className="mt-1 text-sm text-gray-600">
              AI-powered CV analysis and job matching platform powered by AWS Textract and Bedrock
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <Activity 
              className={`h-5 w-5 ${
                stats.apiStatus === 'connected' 
                  ? 'text-green-500' 
                  : stats.apiStatus === 'disconnected'
                  ? 'text-red-500'
                  : 'text-yellow-500'
              }`} 
            />
            <span className={`text-sm font-medium ${
              stats.apiStatus === 'connected' 
                ? 'text-green-600' 
                : stats.apiStatus === 'disconnected'
                ? 'text-red-600'
                : 'text-yellow-600'
            }`}>
              {stats.apiStatus === 'checking' ? 'Checking...' : 
               stats.apiStatus === 'connected' ? 'API Connected' : 'API Disconnected'}
            </span>
          </div>
        </div>
      </div>

      {/* System Status */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <CheckCircle className="h-8 w-8 text-green-500" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">System Status</h3>
              <p className="text-sm text-gray-600">
                {stats.apiStatus === 'connected' ? 'All systems operational' : 'Service unavailable'}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <TrendingUp className="h-8 w-8 text-blue-500" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Performance</h3>
              <p className="text-sm text-gray-600">Fast AI-powered analysis</p>
            </div>
          </div>
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Clock className="h-8 w-8 text-purple-500" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Last Check</h3>
              <p className="text-sm text-gray-600">
                {new Date(stats.lastCheck).toLocaleTimeString()}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div>
        <h2 className="text-lg font-medium text-gray-900 mb-6">Available Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <Link
                key={feature.name}
                to={feature.href}
                className="bg-white shadow rounded-lg p-6 hover:shadow-lg transition-shadow duration-200 group"
              >
                <div className="flex items-center">
                  <div className={`flex-shrink-0 p-3 rounded-lg ${feature.color}`}>
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-medium text-gray-900 group-hover:text-primary-600">
                      {feature.name}
                    </h3>
                    <p className="text-sm text-gray-600 mt-1">
                      {feature.description}
                    </p>
                    <p className="text-xs text-gray-500 mt-2">
                      {feature.stats}
                    </p>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      </div>

      {/* Quick Start Guide */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Quick Start Guide</h2>
        <div className="space-y-4">
          <div className="flex items-start">
            <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
              <span className="text-sm font-medium text-primary-600">1</span>
            </div>
            <div className="ml-4">
              <h4 className="text-sm font-medium text-gray-900">Upload CV</h4>
              <p className="text-sm text-gray-600">Start with CV Analysis to extract skills and experience from a PDF CV</p>
            </div>
          </div>
          
          <div className="flex items-start">
            <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
              <span className="text-sm font-medium text-primary-600">2</span>
            </div>
            <div className="ml-4">
              <h4 className="text-sm font-medium text-gray-900">Job Matching</h4>
              <p className="text-sm text-gray-600">Use Job Matching to compare CVs against specific job requirements</p>
            </div>
          </div>
          
          <div className="flex items-start">
            <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
              <span className="text-sm font-medium text-primary-600">3</span>
            </div>
            <div className="ml-4">
              <h4 className="text-sm font-medium text-gray-900">Batch Processing</h4>
              <p className="text-sm text-gray-600">Process multiple CVs at once for candidate comparison and ranking</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
