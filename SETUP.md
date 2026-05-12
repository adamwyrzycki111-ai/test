# COC Inspector - Quality Inspection & Certificate of Conformance System

A technical MVP demonstrating an industrial Quality Inspection & Certificate of Conformance (COC) workflow for aerospace/manufacturing compliance.

## Quick Start

### Backend (Python/FastAPI)
```bash
cd /workspace/project/test/backend

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000
- API docs: http://localhost:8000/docs

### Frontend (React/Vite)
```bash
cd /workspace/project/test/frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend will be available at: http://localhost:5173

## Features

### 1. Work Order Management
- Select from pre-loaded mock work orders
- View work order details: WO#, Part#, Lot#, Customer

### 2. Document Configuration
Four document types required:
- Electrical Test (generated PDF)
- Mechanical Test (generated PDF)
- FAI Form (generated PDF)
- External Lab Report (uploaded PDF)

### 3. Module PDF Generation
Each document can be generated individually:
- Uses ReportLab for PDF creation
- Includes: title, work order info, table data, inspector signature, timestamp
- Each PDF has distinct visual styling

### 4. External PDF Upload
- Upload external PDFs (e.g., lab reports)
- Stored in NAS folder structure

### 5. Validation
- Validates all required documents before merge
- Blocks merge if any document is missing
- Shows clear error message with missing docs

### 6. Final Merge
- Merges all PDFs into single COC document
- Adds Table of Contents
- Adds page numbers
- Adds bookmarks/outlines
- Uses configured merge order

### 7. Download
- Download final merged COC PDF

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/work-orders | List all work orders |
| GET | /api/work-orders/{wo_number} | Get specific work order |
| GET | /api/documents/{wo_number} | Get all documents for WO |
| GET | /api/validate/{wo_number} | Validate documents exist |
| POST | /api/pdf/generate/electrical | Generate Electrical Test PDF |
| POST | /api/pdf/generate/mechanical | Generate Mechanical Test PDF |
| POST | /api/pdf/generate/fai | Generate FAI Form PDF |
| POST | /api/pdf/upload/{wo_number} | Upload external PDF |
| POST | /api/merge/{wo_number} | Merge into final COC |
| GET | /api/download/{wo_number} | Download final COC PDF |

## Storage Structure

```
/workspace/project/test/storage/nas/
├── generated/
│   └── {work_order_number}/
│       ├── electrical_test.pdf
│       ├── mechanical_test.pdf
│       ├── fai_form.pdf
│       └── external_*.pdf
└── final/
    └── {work_order_number}_COC.pdf
```

## Architecture

### Backend Services
- `document_service.py` - Work order and document management
- `pdf_generator_service.py` - Module PDF generation (ReportLab)
- `merge_service.py` - PDF merge and post-processing (pypdf)

### Frontend
- React + Vite + TypeScript
- Industrial dark theme
- Monospace fonts (JetBrains Mono)

## Tech Stack

- **Backend**: Python 3, FastAPI, ReportLab, pypdf
- **Frontend**: React 18, Vite 6, TypeScript
- **Styling**: CSS (custom industrial theme)
- **Storage**: Local filesystem (simulating NAS)

## Design

The UI follows an industrial aesthetic:
- Dark theme (#0a0f14)
- Sharp corners (no border-radius)
- Status color coding
- Orange primary (#ff6b35)
- JetBrains Mono font

This demonstrates a compliance/QA workflow, not a polished SaaS product.