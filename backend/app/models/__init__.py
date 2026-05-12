from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class DocumentType(str, Enum):
    ELECTRICAL_TEST = "electrical_test"
    MECHANICAL_TEST = "mechanical_test"
    FAI_FORM = "fai_form"
    EXTERNAL_LAB = "external_lab"


class DocumentStatus(str, Enum):
    MISSING = "missing"
    GENERATED = "generated"
    UPLOADED = "uploaded"
    READY = "ready"


class DocumentType2(str, Enum):
    GENERATED = "generated"
    UPLOADED = "uploaded"


class WorkOrder(BaseModel):
    work_order_number: str
    part_number: str
    lot_number: str
    customer: str


class Document(BaseModel):
    id: str
    name: str
    type: DocumentType2
    status: DocumentStatus = DocumentStatus.MISSING
    file_path: Optional[str] = None


class RequiredDocument(BaseModel):
    id: str
    name: str
    type: str  # "generated" or "uploaded"


class ValidationResult(BaseModel):
    valid: bool
    missing_documents: List[str] = []


class MergeOrderConfig(BaseModel):
    order: List[str] = [
        "electrical_test",
        "mechanical_test",
        "fai_form",
        "external_lab"
    ]


class PdfGenerationRequest(BaseModel):
    work_order_number: str


class MergeRequest(BaseModel):
    work_order_number: str


# Test data models for PDF content
class ElectricalTestItem(BaseModel):
    test: str
    spec: str
    result: str
    status: str


class MechanicalTestItem(BaseModel):
    test: str
    spec: str
    result: str
    status: str


class FaiFormItem(BaseModel):
    item: str
    description: str
    spec: str
    actual: str
    status: str


class GenerateElectricalPdfRequest(BaseModel):
    work_order: WorkOrder
    inspector: str = "J. Martinez"
    items: List[ElectricalTestItem]


class GenerateMechanicalPdfRequest(BaseModel):
    work_order: WorkOrder
    inspector: str = "R. Thompson"
    items: List[MechanicalTestItem]


class GenerateFaiPdfRequest(BaseModel):
    work_order: WorkOrder
    inspector: str = "K. Williams"
    items: List[FaiFormItem]