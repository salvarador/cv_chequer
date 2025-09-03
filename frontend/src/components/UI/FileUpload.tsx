import React, { useCallback, useState } from 'react';
import { Upload, X, File, AlertCircle, CheckCircle } from 'lucide-react';
import { validateFileType, validateFileSize, formatFileSize } from '../../utils/helpers';

interface FileUploadProps {
  onFilesSelected: (files: File[]) => void;
  multiple?: boolean;
  maxFiles?: number;
  maxSizeMB?: number;
  accept?: string;
  disabled?: boolean;
  className?: string;
}

interface FileWithError {
  file: File;
  error?: string | null;
}

const FileUpload: React.FC<FileUploadProps> = ({
  onFilesSelected,
  multiple = false,
  maxFiles = 10,
  maxSizeMB = 10,
  accept = '.pdf',
  disabled = false,
  className = ''
}) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState<FileWithError[]>([]);

  const validateFile = (file: File): string | null => {
    if (!validateFileType(file)) {
      return 'Only PDF files are allowed';
    }
    
    if (!validateFileSize(file, maxSizeMB)) {
      return `File size must be less than ${maxSizeMB}MB`;
    }
    
    return null;
  };

  const handleFiles = useCallback((files: FileList | null) => {
    if (!files) return;

    const fileArray = Array.from(files);
    const filesToProcess = multiple ? fileArray.slice(0, maxFiles) : [fileArray[0]];
    
    const filesWithErrors: FileWithError[] = filesToProcess.map(file => ({
      file,
      error: validateFile(file)
    }));

    setSelectedFiles(filesWithErrors);
    
    // Only pass valid files to parent component
    const validFiles = filesWithErrors
      .filter(item => !item.error)
      .map(item => item.file);
    
    onFilesSelected(validFiles);
  }, [multiple, maxFiles, maxSizeMB, onFilesSelected]);

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
    
    if (disabled) return;
    
    const files = e.dataTransfer.files;
    handleFiles(files);
  }, [disabled, handleFiles]);

  const handleFileInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    handleFiles(files);
  }, [handleFiles]);

  const removeFile = useCallback((index: number) => {
    const newFiles = selectedFiles.filter((_, i) => i !== index);
    setSelectedFiles(newFiles);
    
    const validFiles = newFiles
      .filter(item => !item.error)
      .map(item => item.file);
    
    onFilesSelected(validFiles);
  }, [selectedFiles, onFilesSelected]);

  return (
    <div className={`space-y-4 ${className}`}>
      <div
        className={`
          relative border-2 border-dashed rounded-lg p-6 transition-all duration-200
          ${isDragOver && !disabled
            ? 'border-primary-400 bg-primary-50'
            : 'border-gray-300 hover:border-gray-400'
          }
          ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
        `}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        <input
          type="file"
          multiple={multiple}
          accept={accept}
          onChange={handleFileInputChange}
          disabled={disabled}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />
        
        <div className="text-center">
          <Upload className={`mx-auto h-12 w-12 ${disabled ? 'text-gray-300' : 'text-gray-400'}`} />
          <div className="mt-4">
            <p className={`text-lg font-medium ${disabled ? 'text-gray-400' : 'text-gray-900'}`}>
              {isDragOver ? 'Drop files here' : 'Upload CV files'}
            </p>
            <p className={`mt-2 text-sm ${disabled ? 'text-gray-400' : 'text-gray-600'}`}>
              Drag and drop or{' '}
              <span className="font-medium text-primary-600 hover:text-primary-500">
                browse
              </span>{' '}
              to choose files
            </p>
            <p className={`mt-1 text-xs ${disabled ? 'text-gray-400' : 'text-gray-500'}`}>
              PDF files only, max {maxSizeMB}MB each
              {multiple && ` (up to ${maxFiles} files)`}
            </p>
          </div>
        </div>
      </div>

      {/* Selected Files List */}
      {selectedFiles.length > 0 && (
        <div className="space-y-2">
          <h4 className="text-sm font-medium text-gray-900">Selected Files:</h4>
          <div className="space-y-2">
            {selectedFiles.map((fileItem, index) => (
              <div
                key={index}
                className={`flex items-center justify-between p-3 rounded-lg border ${
                  fileItem.error ? 'border-red-200 bg-red-50' : 'border-gray-200 bg-gray-50'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <File className={`h-5 w-5 ${fileItem.error ? 'text-red-500' : 'text-gray-500'}`} />
                  <div>
                    <p className={`text-sm font-medium ${fileItem.error ? 'text-red-900' : 'text-gray-900'}`}>
                      {fileItem.file.name}
                    </p>
                    <p className={`text-xs ${fileItem.error ? 'text-red-600' : 'text-gray-600'}`}>
                      {formatFileSize(fileItem.file.size)}
                    </p>
                    {fileItem.error && (
                      <p className="text-xs text-red-600 mt-1 flex items-center">
                        <AlertCircle className="h-3 w-3 mr-1" />
                        {fileItem.error}
                      </p>
                    )}
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  {!fileItem.error && (
                    <CheckCircle className="h-5 w-5 text-green-500" />
                  )}
                  <button
                    type="button"
                    onClick={() => removeFile(index)}
                    className="p-1 rounded-full hover:bg-gray-200 transition-colors"
                  >
                    <X className="h-4 w-4 text-gray-500" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
