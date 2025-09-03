// Re-export all types from the API service for easier imports
export * from '../services/api';

// Additional types for UI components
export interface LoadingState {
  isLoading: boolean;
  message?: string;
}

export interface ErrorState {
  hasError: boolean;
  message?: string;
  details?: string;
}

export interface FileUploadState {
  files: File[];
  isUploading: boolean;
  uploadProgress: number;
  error?: string;
}

export interface NavigationItem {
  name: string;
  href: string;
  icon?: React.ComponentType<React.SVGProps<SVGSVGElement>>;
  current: boolean;
}

export interface PageProps {
  title?: string;
  description?: string;
}
