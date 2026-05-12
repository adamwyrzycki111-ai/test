"""
FastAPI Application for COC System
"""

import os
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import List

from app.models import (
    WorkOrder, Document, ValidationResult,
    ElectricalTestItem, MechanicalTestItem, FaiFormItem,
    PdfGenerationRequest, MergeRequest
)
from app.services.document_service import document_service, GENERATED_PATH, FINAL_PATH
from app.services.pdf_generator_service import pdf_generator_service
from app.services.merge_service import merge_service


app = FastAPI(
    title="COC Inspector API",
    description="Quality Inspection & Certificate of Conformance System",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================== Work Order Endpoints ==================

@app.get("/api/work-orders", response_model=List[WorkOrder])
async def get_work_orders():
    """Get all work orders"""
    return document_service.get_work_orders()


@app.get("/api/work-orders/{work_order_number}", response_model=WorkOrder)
async def get_work_order(work_order_number: str):
    """Get a specific work order"""
    work_order = document_service.get_work_order(work_order_number)
    if not work_order:
        raise HTTPException(status_code=404, detail="Work order not found")
    return work_order


# ================== Document Endpoints ==================

@app.get("/api/documents/{work_order_number}", response_model=List[Document])
async def get_documents(work_order_number: str):
    """Get all documents for a work order"""
    return document_service.get_all_documents(work_order_number)


@app.get("/api/documents/{work_order_number}/{document_id}", response_model=Document)
async def get_document(work_order_number: str, document_id: str):
    """Get a specific document"""
    return document_service.get_document(work_order_number, document_id)


@app.get("/api/validate/{work_order_number}", response_model=ValidationResult)
async def validate_documents(work_order_number: str):
    """Validate all required documents exist"""
    return document_service.validate_documents(work_order_number)


# ================== PDF Generation Endpoints ==================

@app.post("/api/pdf/generate/electrical")
async def generate_electrical_pdf(request: PdfGenerationRequest):
    """Generate Electrical Test PDF"""
    work_order = document_service.get_work_order(request.work_order_number)
    if not work_order:
        raise HTTPException(status_code=404, detail="Work order not found")
    
    # Create default test items
    items = [
        ElectricalTestItem(test="Insulation Resistance", spec=">100MΩ", result="147MΩ", status="PASS"),
        ElectricalTestItem(test="Dielectric Strength", spec="1500VAC", result="1520VAC", status="PASS"),
        ElectricalTestItem(test="Continuity", spec="<0.1Ω", result="0.042Ω", status="PASS"),
        ElectricalTestItem(test="Ground Continuity", spec="<0.5Ω", result="0.18Ω", status="PASS"),
        ElectricalTestItem(test="Hipot Test", spec="1500VAC/1min", result="PASS", status="PASS"),
    ]
    
    file_path = pdf_generator_service.generate_electrical_test_pdf(work_order, items=items)
    
    return {
        "success": True,
        "document_id": "electrical_test",
        "file_path": file_path
    }


@app.post("/api/pdf/generate/mechanical")
async def generate_mechanical_pdf(request: PdfGenerationRequest):
    """Generate Mechanical Test PDF"""
    work_order = document_service.get_work_order(request.work_order_number)
    if not work_order:
        raise HTTPException(status_code=404, detail="Work order not found")
    
    # Create default test items
    items = [
        MechanicalTestItem(test="Dimensional Check", spec="±0.05mm", result="+0.02mm", status="PASS"),
        MechanicalTestItem(test="Torque Test", spec="15-20 Nm", result="17.5 Nm", status="PASS"),
        MechanicalTestItem(test="Thread Inspection", spec="No defects", result="No defects found", status="PASS"),
        MechanicalTestItem(test="Visual Inspection", spec="Per ASME", result="Compliant", status="PASS"),
        MechanicalTestItem(test="Hardness Test", spec="55-65 HRC", result="58 HRC", status="PASS"),
    ]
    
    file_path = pdf_generator_service.generate_mechanical_test_pdf(work_order, items=items)
    
    return {
        "success": True,
        "document_id": "mechanical_test",
        "file_path": file_path
    }


@app.post("/api/pdf/generate/fai")
async def generate_fai_pdf(request: PdfGenerationRequest):
    """Generate FAI Form PDF"""
    work_order = document_service.get_work_order(request.work_order_number)
    if not work_order:
        raise HTTPException(status_code=404, detail="Work order not found")
    
    # Create default FAI items
    items = [
        FaiFormItem(item="1", description="Main Body Assembly", spec="Per drawing", actual="Conforms", status="APPROVED"),
        FaiFormItem(item="2", description="Mounting Brackets", spec="Per drawing", actual="Conforms", status="APPROVED"),
        FaiFormItem(item="3", description="Fasteners", spec="Per spec", actual="Conforms", status="APPROVED"),
        FaiFormItem(item="4", description="Seals", spec="Per spec", actual="Conforms", status="APPROVED"),
        FaiFormItem(item="5", description="Finish", spec="Per MIL-PRF", actual="Conforms", status="APPROVED"),
        FaiFormItem(item="6", description="Marking", spec="Per spec", actual="Conforms", status="APPROVED"),
    ]
    
    file_path = pdf_generator_service.generate_fai_form_pdf(work_order, items=items)
    
    return {
        "success": True,
        "document_id": "fai_form",
        "file_path": file_path
    }


# ================== External PDF Upload ==================

@app.post("/api/pdf/upload/{work_order_number}")
async def upload_external_pdf(
    work_order_number: str,
    file: UploadFile = File(...)
):
    """Upload an external PDF (e.g., Lab Report)"""
    work_order = document_service.get_work_order(work_order_number)
    if not work_order:
        raise HTTPException(status_code=404, detail="Work order not found")
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Save the file
    folder = document_service.get_document_folder(work_order_number)
    
    # Sanitize filename
    safe_filename = file.filename.replace(' ', '_')
    file_path = f"{folder}/external_{safe_filename}"
    
    # Save uploaded file
    content = await file.read()
    with open(file_path, 'wb') as f:
        f.write(content)
    
    return {
        "success": True,
        "document_id": "external_lab",
        "file_path": file_path,
        "filename": safe_filename
    }


# ================== Merge Endpoints ==================

@app.post("/api/merge/{work_order_number}")
async def merge_documents(work_order_number: str):
    """Merge all documents into final COC PDF"""
    work_order = document_service.get_work_order(work_order_number)
    if not work_order:
        raise HTTPException(status_code=404, detail="Work order not found")
    
    # Validate documents first
    validation = document_service.validate_documents(work_order_number)
    if not validation.valid:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Cannot generate final COC. Missing required documents:",
                "missing_documents": validation.missing_documents
            }
        )
    
    # Get files in merge order
    files_with_titles = document_service.get_files_for_merge(work_order_number)
    
    if not files_with_titles:
        raise HTTPException(status_code=400, detail="No documents to merge")
    
    # Merge PDFs
    output_path = merge_service.merge_pdfs(files_with_titles, work_order_number)
    
    return {
        "success": True,
        "work_order_number": work_order_number,
        "output_path": output_path,
        "message": "Final COC PDF generated successfully"
    }


@app.get("/api/download/{work_order_number}")
async def download_coc(work_order_number: str):
    """Download the final COC PDF"""
    final_folder = document_service.get_final_folder()
    file_path = f"{final_folder}/{work_order_number}_COC.pdf"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="COC not found. Generate it first.")
    
    return FileResponse(
        file_path,
        filename=f"{work_order_number}_COC.pdf",
        media_type='application/pdf'
    )


# ================== Service Info ==================

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "COC Inspector API",
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "COC Inspector API",
        "version": "1.0.0",
        "docs": "/docs"
    }