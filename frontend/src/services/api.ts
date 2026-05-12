// API Service for communicating with COC Backend

const API_BASE = 'http://localhost:8000/api';

async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || error.message || 'API request failed');
  }
  
  return response.json();
}

// Work Orders
export async function getWorkOrders() {
  return fetchAPI<import('../types').WorkOrder[]>('/work-orders');
}

export async function getWorkOrder(workOrderNumber: string) {
  return fetchAPI<import('../types').WorkOrder>(`/work-orders/${workOrderNumber}`);
}

// Documents
export async function getDocuments(workOrderNumber: string) {
  return fetchAPI<import('../types').Document[]>(`/documents/${workOrderNumber}`);
}

export async function validateDocuments(workOrderNumber: string) {
  return fetchAPI<import('../types').ValidationResult>(`/validate/${workOrderNumber}`);
}

// PDF Generation
export async function generateElectricalPdf(workOrderNumber: string) {
  return fetchAPI<{ success: boolean; document_id: string; file_path: string }>('/pdf/generate/electrical', {
    method: 'POST',
    body: JSON.stringify({ work_order_number: workOrderNumber }),
  });
}

export async function generateMechanicalPdf(workOrderNumber: string) {
  return fetchAPI<{ success: boolean; document_id: string; file_path: string }>('/pdf/generate/mechanical', {
    method: 'POST',
    body: JSON.stringify({ work_order_number: workOrderNumber }),
  });
}

export async function generateFaiPdf(workOrderNumber: string) {
  return fetchAPI<{ success: boolean; document_id: string; file_path: string }>('/pdf/generate/fai', {
    method: 'POST',
    body: JSON.stringify({ work_order_number: workOrderNumber }),
  });
}

// External Upload
export async function uploadExternalPdf(workOrderNumber: string, file: File) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_BASE}/pdf/upload/${workOrderNumber}`, {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
    throw new Error(error.detail || 'Upload failed');
  }
  
  return response.json();
}

// Merge
export async function mergeDocuments(workOrderNumber: string) {
  return fetchAPI<import('../types').MergeResult>(`/merge/${workOrderNumber}`, {
    method: 'POST',
  });
}

// Download
export function getDownloadUrl(workOrderNumber: string) {
  return `${API_BASE}/download/${workOrderNumber}`;
}

// Health
export async function healthCheck() {
  return fetchAPI<{ status: string }>('/health');
}