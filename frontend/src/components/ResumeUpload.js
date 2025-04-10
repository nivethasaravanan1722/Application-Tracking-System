import React, { useState, useCallback } from 'react';
import { ArrowUpTrayIcon, DocumentTextIcon, XMarkIcon } from '@heroicons/react/24/outline';

const ResumeUpload = () => {
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState(null);
  const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB in bytes

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback(() => {
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFile = e.dataTransfer.files[0];
      validateAndSetFile(droppedFile);
    }
  }, []);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (file) => {
    setError(null);
    
    if (file.type !== 'application/pdf') {
      setError('Only PDF files are supported');
      return;
    }
    
    if (file.size > MAX_FILE_SIZE) {
      setError('File size exceeds 5MB limit');
      return;
    }
    
    setFile(file);
  };

  const removeFile = useCallback(() => {
    setFile(null);
    setError(null);
  }, []);

  return (
    <div className="max-w-lg mx-auto p-6 bg-white rounded-xl shadow-md">
      <h2 className="text-xl font-semibold text-gray-800 mb-4 text-center">Upload Your Resume</h2>

      <div
        className={`border-2 border-dashed rounded-lg p-6 text-center transition-all ${
          isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400'
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => document.getElementById('fileInput')?.click()}
        role="button"
        tabIndex={0}
        aria-label="Upload resume"
      >
        {!file ? (
          <div className="space-y-2">
            <ArrowUpTrayIcon className={`mx-auto h-10 w-10 ${
              isDragging ? 'text-blue-500' : 'text-gray-400'
            }`} />
            <p className="text-sm text-gray-600">
              {isDragging ? 'Drop your resume here' : 'Drag & drop your resume here'}
            </p>
            <p className="text-xs text-gray-500">or</p>
            <label
              htmlFor="fileInput"
              className="inline-block mt-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 cursor-pointer"
            >
              Browse Files
            </label>
            <input
              type="file"
              accept="application/pdf"
              id="fileInput"
              className="hidden"
              onChange={handleFileChange}
            />
          </div>
        ) : (
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
            <div className="flex items-center gap-3">
              <DocumentTextIcon className="h-6 w-6 text-blue-600 flex-shrink-0" />
              <div className="text-left overflow-hidden">
                <p className="text-sm font-medium text-gray-800 truncate">{file.name}</p>
                <p className="text-xs text-gray-500">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation();
                removeFile();
              }}
              className="text-gray-400 hover:text-red-500 transition-colors p-1"
              aria-label="Remove file"
            >
              <XMarkIcon className="h-5 w-5" />
            </button>
          </div>
        )}
      </div>

      {error && (
        <p className="text-xs text-red-500 mt-2 text-center">{error}</p>
      )}

      <div className="mt-4 text-xs text-gray-500 text-center">
        <p>Supported format: PDF (max 5MB)</p>
      </div>

      {file && (
        <button
          className="w-full mt-4 py-2 px-4 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 transition-colors"
          onClick={() => {
            // Here you would typically handle the upload
            console.log('Uploading:', file.name);
          }}
        >
          Process Resume
        </button>
      )}
    </div>
  );
};

export default ResumeUpload;