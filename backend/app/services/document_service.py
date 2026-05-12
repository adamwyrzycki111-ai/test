import os
import json
from typing import List, Dict, Optional
from ..models import WorkOrder, Document, RequiredDocument, DocumentStatus, ValidationResult, DocumentType2


# Base storage paths
STORAGE_BASE = "/workspace/project/test/storage/nas"
GENERATED_PATH = f"{STORAGE_BASE}/generated"
FINAL_PATH = f"{STORAGE_BASE}/final"


class DocumentService:
    """Service for managing work orders and documents"""
    
    def __init__(self):
        self.work_orders = self._init_mock_work_orders()
        self.required_documents = self._init_required_documents()
    
    def _init_mock_work_orders(self) -> List[WorkOrder]:
        return [
            WorkOrder(
                work_order_number="WO-2024-001847",
                part_number="PN-AS-8847-A",
                lot_number="LOT-2024-0347",
                customer="AeroSpace Dynamics Inc."
            ),
            WorkOrder(
                work_order_number="WO-2024-001848",
                part_number="PN-AS-9921-B",
                lot_number="LOT-2024-0348",
                customer="Global Aerospace Ltd."
            ),
            WorkOrder(
                work_order_number="WO-2024-001849",
                part_number="PN-HD-4420-C",
                lot_number="LOT-2024-0349",
                customer="Precision Manufacturing Co."
            )
        ]
    
    def _init_required_documents(self) -> List[RequiredDocument]:
        return [
            RequiredDocument(id="electrical_test", name="Electrical Test", type="generated"),
            RequiredDocument(id="mechanical_test", name="Mechanical Test", type="generated"),
            RequiredDocument(id="fai_form", name="FAI Form", type="generated"),
            RequiredDocument(id="external_lab", name="External Lab Report", type="uploaded")
        ]
    
    def get_work_orders(self) -> List[WorkOrder]:
        return self.work_orders
    
    def get_work_order(self, work_order_number: str) -> Optional[WorkOrder]:
        for wo in self.work_orders:
            if wo.work_order_number == work_order_number:
                return wo
        return None
    
    def get_required_documents(self) -> List[RequiredDocument]:
        return self.required_documents
    
    def get_document_folder(self, work_order_number: str) -> str:
        folder = f"{GENERATED_PATH}/{work_order_number}"
        os.makedirs(folder, exist_ok=True)
        return folder
    
    def get_final_folder(self) -> str:
        os.makedirs(FINAL_PATH, exist_ok=True)
        return FINAL_PATH
    
    def get_document(self, work_order_number: str, document_id: str) -> Document:
        """Get document status for a work order"""
        required_doc = next((d for d in self.required_documents if d.id == document_id), None)
        if not required_doc:
            return Document(
                id=document_id,
                name=document_id,
                type=DocumentType2.GENERATED,
                status=DocumentStatus.MISSING
            )
        
        # Check if file exists
        doc_type = DocumentType2(required_doc.type)
        folder = self.get_document_folder(work_order_number)
        
        if doc_type == DocumentType2.UPLOADED:
            # For uploaded docs, check for external_*.pdf files
            files = [f for f in os.listdir(folder) if f.startswith("external_") and f.endswith(".pdf")]
            if files:
                file_path = f"{folder}/{files[0]}"
                return Document(
                    id=document_id,
                    name=required_doc.name,
                    type=doc_type,
                    status=DocumentStatus.UPLOADED,
                    file_path=file_path
                )
        else:
            # For generated docs, check for specific file
            file_path = f"{folder}/{document_id}.pdf"
            if os.path.exists(file_path):
                return Document(
                    id=document_id,
                    name=required_doc.name,
                    type=doc_type,
                    status=DocumentStatus.GENERATED,
                    file_path=file_path
                )
        
        return Document(
            id=document_id,
            name=required_doc.name,
            type=doc_type,
            status=DocumentStatus.MISSING
        )
    
    def get_all_documents(self, work_order_number: str) -> List[Document]:
        """Get all documents for a work order"""
        documents = []
        for required_doc in self.required_documents:
            doc = self.get_document(work_order_number, required_doc.id)
            documents.append(doc)
        return documents
    
    def validate_documents(self, work_order_number: str) -> ValidationResult:
        """Validate all required documents exist"""
        documents = self.get_all_documents(work_order_number)
        missing = [d.name for d in documents if d.status == DocumentStatus.MISSING]
        return ValidationResult(
            valid=len(missing) == 0,
            missing_documents=missing
        )
    
    def get_merge_order(self) -> List[str]:
        """Get the configured merge order"""
        return ["electrical_test", "mechanical_test", "fai_form", "external_lab"]
    
    def get_files_for_merge(self, work_order_number: str) -> List[tuple]:
        """Get files in the correct merge order"""
        order = self.get_merge_order()
        files = []
        folder = self.get_document_folder(work_order_number)
        
        for doc_id in order:
            required_doc = next((d for d in self.required_documents if d.id == doc_id), None)
            if not required_doc:
                continue
            
            doc_type = DocumentType2(required_doc.type)
            
            if doc_type == DocumentType2.UPLOADED:
                uploaded_files = [f for f in os.listdir(folder) if f.startswith("external_") and f.endswith(".pdf")]
                if uploaded_files:
                    files.append((f"{folder}/{uploaded_files[0]}", required_doc.name))
            else:
                file_path = f"{folder}/{doc_id}.pdf"
                if os.path.exists(file_path):
                    files.append((file_path, required_doc.name))
        
        return files


# Singleton instance
document_service = DocumentService()