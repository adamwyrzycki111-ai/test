// Main App Component - COC Inspector Application

import { useState, useEffect, useCallback } from 'react';
import './App.css';
import { Header } from './components/Header';
import { WorkOrderPanel } from './components/WorkOrderPanel';
import { DocumentCard } from './components/DocumentCard';
import type { WorkOrder, Document } from './types';
import * as api from './services/api';

function App() {
  const [workOrders, setWorkOrders] = useState<WorkOrder[]>([]);
  const [selectedWorkOrder, setSelectedWorkOrder] = useState<WorkOrder | null>(null);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [validation, setValidation] = useState<{ valid: boolean; missing_documents: string[] } | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isMerging, setIsMerging] = useState(false);
  const [mergeError, setMergeError] = useState<string | null>(null);
  const [mergeSuccess, setMergeSuccess] = useState(false);
  const [cocExists, setCocExists] = useState(false);

  // Load work orders on mount
  useEffect(() => {
    async function loadWorkOrders() {
      try {
        const wos = await api.getWorkOrders();
        setWorkOrders(wos);
        if (wos.length > 0) {
          setSelectedWorkOrder(wos[0]);
        }
      } catch (error) {
        console.error('Failed to load work orders:', error);
      } finally {
        setIsLoading(false);
      }
    }
    loadWorkOrders();
  }, []);

  // Load documents when work order changes
  useEffect(() => {
    async function loadDocuments() {
      if (!selectedWorkOrder) return;
      try {
        const docs = await api.getDocuments(selectedWorkOrder.work_order_number);
        setDocuments(docs);
        
        const validation = await api.validateDocuments(selectedWorkOrder.work_order_number);
        setValidation(validation);
        
        // Reset merge state
        setCocExists(false);
        setMergeSuccess(false);
        setMergeError(null);
      } catch (error) {
        console.error('Failed to load documents:', error);
      }
    }
    loadDocuments();
  }, [selectedWorkOrder]);

  const refreshDocuments = useCallback(async () => {
    if (!selectedWorkOrder) return;
    try {
      const docs = await api.getDocuments(selectedWorkOrder.work_order_number);
      setDocuments(docs);
      
      const validation = await api.validateDocuments(selectedWorkOrder.work_order_number);
      setValidation(validation);
    } catch (error) {
      console.error('Failed to refresh documents:', error);
    }
  }, [selectedWorkOrder]);

  const handleGenerate = async (_docId: string) => {
    if (!selectedWorkOrder) return;
    
    setIsGenerating(true);
    try {
      switch (_docId) {
        case 'electrical_test':
          await api.generateElectricalPdf(selectedWorkOrder.work_order_number);
          break;
        case 'mechanical_test':
          await api.generateMechanicalPdf(selectedWorkOrder.work_order_number);
          break;
        case 'fai_form':
          await api.generateFaiPdf(selectedWorkOrder.work_order_number);
          break;
      }
      await refreshDocuments();
    } catch (error) {
      console.error(`Failed to generate ${_docId}:`, error);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleUpload = async (_docId: string, file: File) => {
    if (!selectedWorkOrder) return;
    
    try {
      await api.uploadExternalPdf(selectedWorkOrder.work_order_number, file);
      await refreshDocuments();
    } catch (error) {
      console.error('Failed to upload:', error);
    }
  };

  const handleMerge = async () => {
    if (!selectedWorkOrder) return;
    
    setIsMerging(true);
    setMergeError(null);
    try {
      await api.mergeDocuments(selectedWorkOrder.work_order_number);
      setMergeSuccess(true);
      setCocExists(true);
    } catch (error: any) {
      if (error.message && error.message.includes('Missing required documents')) {
        setMergeError(error.message);
      } else {
        setMergeError('Merge failed: ' + (error.message || 'Unknown error'));
      }
    } finally {
      setIsMerging(false);
    }
  };

  const handleDownload = () => {
    if (!selectedWorkOrder) return;
    const url = api.getDownloadUrl(selectedWorkOrder.work_order_number);
    window.open(url, '_blank');
  };

  if (isLoading) {
    return (
      <div className="app">
        <Header />
        <div className="loading">
          <span className="loading-text">INITIALIZING COC INSPECTOR...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <Header workOrderNumber={selectedWorkOrder?.work_order_number} />
      
      <main className="main-content">
        {/* Work Order Selector */}
        <div className="section wo-selector">
          <label className="section-label">SELECT WORK ORDER</label>
          <select 
            className="wo-select"
            value={selectedWorkOrder?.work_order_number || ''}
            onChange={(e) => {
              const wo = workOrders.find(w => w.work_order_number === e.target.value);
              if (wo) setSelectedWorkOrder(wo);
            }}
          >
            {workOrders.map(wo => (
              <option key={wo.work_order_number} value={wo.work_order_number}>
                {wo.work_order_number} - {wo.part_number}
              </option>
            ))}
          </select>
        </div>

        {/* Work Order Panel */}
        {selectedWorkOrder && (
          <WorkOrderPanel workOrder={selectedWorkOrder} />
        )}

        {/* Documents Section */}
        <div className="section">
          <div className="section-header">
            <span className="section-label">REQUIRED DOCUMENTS</span>
            <span className="section-count">
              {documents.filter(d => d.status !== 'missing').length} / {documents.length} COMPLETED
            </span>
          </div>
          
          {/* Validation Error */}
          {validation && !validation.valid && (
            <div className="validation-error">
              <span className="error-title">⚠ VALIDATION FAILED</span>
              <span className="error-subtitle">Missing required documents:</span>
              <ul className="error-list">
                {validation.missing_documents.map(doc => (
                  <li key={doc}>{doc}</li>
                ))}
              </ul>
            </div>
          )}
          
          {/* Document Cards Grid */}
          <div className="documents-grid">
            {documents.map(doc => (
              <DocumentCard
                key={doc.id}
                document={doc}
                workOrderNumber={selectedWorkOrder?.work_order_number || ''}
                onGenerate={handleGenerate}
                onUpload={handleUpload}
                isGenerating={isGenerating}
              />
            ))}
          </div>
        </div>

        {/* Merge Section */}
        <div className="section merge-section">
          <div className="section-header">
            <span className="section-label">FINAL COC GENERATION</span>
          </div>
          
          {/* Merge Error Display */}
          {mergeError && (
            <div className="merge-error">
              <span className="error-icon">⛔</span>
              <span className="error-message">{mergeError}</span>
            </div>
          )}
          
          {/* Merge Success Display */}
          {mergeSuccess && cocExists && (
            <div className="merge-success">
              <span className="success-icon">✓</span>
              <span className="success-message">COC GENERATED SUCCESSFULLY</span>
            </div>
          )}
          
          {/* Merge Actions */}
          <div className="merge-actions">
            <button 
              className="btn-merge"
              onClick={handleMerge}
              disabled={isMerging || validation?.valid === false}
            >
              {isMerging ? 'MERGING DOCUMENTS...' : 'GENERATE FINAL COC'}
            </button>
            
            {mergeSuccess && (
              <button 
                className="btn-download"
                onClick={handleDownload}
              >
                ↓ DOWNLOAD COC PDF
              </button>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="footer">
        <span>COC INSPECTOR v1.0 | QUALITY ASSURANCE SYSTEM</span>
        <span className="footer-divider">|</span>
        <span>{new Date().getFullYear()}</span>
      </footer>
    </div>
  );
}

export default App;