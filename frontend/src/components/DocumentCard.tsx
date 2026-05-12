// DocumentCard Component - Shows individual document status

import { useState } from 'react';
import type { Document } from '../types';
import './DocumentCard.css';

interface DocumentCardProps {
  document: Document;
  workOrderNumber: string;
  onGenerate: (docId: string) => Promise<void>;
  onUpload: (docId: string, file: File) => Promise<void>;
  isGenerating: boolean;
}

export function DocumentCard({ 
  document, 
  workOrderNumber: _workOrderNumber,
  onGenerate, 
  onUpload,
  isGenerating 
}: DocumentCardProps) {
  const [isUploading, setIsUploading] = useState(false);
  const [showFileInput, setShowFileInput] = useState(false);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setIsUploading(true);
      try {
        await onUpload(document.id, file);
        setShowFileInput(false);
      } catch (error) {
        console.error('Upload failed:', error);
      } finally {
        setIsUploading(false);
      }
    }
  };

  const statusClass = `status-${document.status}`;
  const isGenerated = document.type === 'generated';
  const isUploaded = document.type === 'uploaded';

  return (
    <div className={`document-card ${statusClass}`}>
      <div className="card-header">
        <span className="card-name">{document.name}</span>
        <span className={`card-type-badge ${isGenerated ? 'type-generated' : 'type-uploaded'}`}>
          {isGenerated ? 'GENERATED' : 'UPLOADED'}
        </span>
      </div>
      
      <div className="card-status">
        <span className={`status-indicator ${statusClass}`}>
          {document.status === 'missing' && '●'}
          {document.status === 'generated' && '◉'}
          {document.status === 'uploaded' && '◉'}
          {document.status === 'ready' && '◉'}
        </span>
        <span className={`status-text ${statusClass}`}>
          {document.status.toUpperCase()}
        </span>
      </div>

      <div className="card-actions">
        {isGenerated && document.status === 'missing' && (
          <button 
            className="btn-generate"
            onClick={() => onGenerate(document.id)}
            disabled={isGenerating}
          >
            {isGenerating ? 'GENERATING...' : 'GENERATE PDF'}
          </button>
        )}
        
        {isGenerated && document.status === 'generated' && (
          <span className="card-completed">
            ✓ PDF GENERATED
          </span>
        )}
        
        {isUploaded && document.status === 'missing' && !showFileInput && (
          <button 
            className="btn-upload"
            onClick={() => setShowFileInput(true)}
          >
            UPLOAD PDF
          </button>
        )}
        
        {showFileInput && (
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            className="file-input"
            disabled={isUploading}
          />
        )}
        
        {isUploaded && document.status === 'uploaded' && (
          <span className="card-completed">
            ✓ PDF UPLOADED
          </span>
        )}
      </div>
    </div>
  );
}
