// Utility functions for the CV Chequer application

/**
 * Format file size in human readable format
 */
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

/**
 * Format date to local string
 */
export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
};

/**
 * Get color class based on score percentage
 */
export const getScoreColor = (score: number): string => {
  if (score >= 80) return 'text-green-600';
  if (score >= 60) return 'text-yellow-600';
  if (score >= 40) return 'text-orange-600';
  return 'text-red-600';
};

/**
 * Get background color class based on score percentage
 */
export const getScoreBgColor = (score: number): string => {
  if (score >= 80) return 'bg-green-100';
  if (score >= 60) return 'bg-yellow-100';
  if (score >= 40) return 'bg-orange-100';
  return 'bg-red-100';
};

/**
 * Get importance color based on importance level
 */
export const getImportanceColor = (importance: string): string => {
  switch (importance.toLowerCase()) {
    case 'critical':
    case 'high':
      return 'text-red-600 bg-red-100';
    case 'medium':
      return 'text-yellow-600 bg-yellow-100';
    case 'low':
      return 'text-green-600 bg-green-100';
    default:
      return 'text-gray-600 bg-gray-100';
  }
};

/**
 * Validate file type (only PDF)
 */
export const validateFileType = (file: File): boolean => {
  return file.type === 'application/pdf';
};

/**
 * Validate file size (max 10MB)
 */
export const validateFileSize = (file: File, maxSizeMB: number = 10): boolean => {
  const maxSizeBytes = maxSizeMB * 1024 * 1024;
  return file.size <= maxSizeBytes;
};

/**
 * Calculate overall progress for multiple files
 */
export const calculateOverallProgress = (filesProgress: number[]): number => {
  if (filesProgress.length === 0) return 0;
  const total = filesProgress.reduce((sum, progress) => sum + progress, 0);
  return Math.round(total / filesProgress.length);
};

/**
 * Debounce function for search/input handling
 */
export const debounce = <T extends (...args: any[]) => void>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: NodeJS.Timeout;
  
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
};

/**
 * Truncate text to specified length
 */
export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

/**
 * Convert camelCase to Title Case
 */
export const camelToTitle = (str: string): string => {
  return str
    .replace(/([A-Z])/g, ' $1')
    .replace(/^./, (firstChar) => firstChar.toUpperCase())
    .trim();
};

/**
 * Sort array by score descending
 */
export const sortByScore = <T extends { score?: number; overall_score?: number }>(items: T[]): T[] => {
  return [...items].sort((a, b) => {
    const scoreA = a.score ?? a.overall_score ?? 0;
    const scoreB = b.score ?? b.overall_score ?? 0;
    return scoreB - scoreA;
  });
};

/**
 * Group items by category
 */
export const groupByCategory = <T extends Record<string, any>>(
  items: T[],
  categoryKey: string
): Record<string, T[]> => {
  return items.reduce((groups, item) => {
    const category = item[categoryKey] || 'Other';
    if (!groups[category]) {
      groups[category] = [];
    }
    groups[category].push(item);
    return groups;
  }, {} as Record<string, T[]>);
};

/**
 * Check if the application is running in development mode
 */
export const isDevelopment = (): boolean => {
  return import.meta.env.MODE === 'development';
};

/**
 * Get API base URL from environment
 */
export const getApiBaseUrl = (): string => {
  return import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
};
