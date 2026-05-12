// Type definitions for COC Inspector

export interface WorkOrder {
  work_order_number: string;
  part_number: string;
  lot_number: string;
  customer: string;
}

export interface Document {
  id: string;
  name: string;
  type: 'generated' | 'uploaded';
  status: DocumentStatus;
  file_path?: string;
}

export type DocumentStatus = 'missing' | 'generated' | 'uploaded' | 'ready';

export interface ValidationResult {
  valid: boolean;
  missing_documents: string[];
}

export interface MergeResult {
  success: boolean;
  work_order_number: string;
  output_path: string;
  message: string;
}

export interface ElectricalTestItem {
  test: string;
  spec: string;
  result: string;
  status: string;
}

export interface MechanicalTestItem {
  test: string;
  spec: string;
  result: string;
  status: string;
}

export interface FaiFormItem {
  item: string;
  description: string;
  spec: string;
  actual: string;
  status: string;
}