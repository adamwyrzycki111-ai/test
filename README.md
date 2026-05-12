# COC Inspector - Quality Inspection & Certificate of Conformance System

## Quick Start

### Backend
```bash
cd /workspace/project/test/backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd /workspace/project/test/frontend
npm install
npm run build
npx serve dist
```

Or for dev: `npm run dev`

## Features Demo'd

1. **Work Order Screen** - Select WO, view part/lot/customer
2. **Module PDF Generation** - Electrical, Mechanical, FAI PDFs (ReportLab)
3. **External PDF Upload** - Upload lab reports
4. **Validation** - Blocks merge if docs missing
5. **PDF Merge** - Combines all into single COC with TOC, page numbers
6. **Download** - Get final merged PDF

## Status

- Backend: ✓ Running on localhost:8000
- Frontend: ✓ Built to dist/
- Merge: ✓ Generates WO-2024-001847_COC.pdf

## Tech Stack
- Backend: Python 3, FastAPI, ReportLab, pypdf
- Frontend: React 18, Vite 6, TypeScript
- Storage: Local filesystem (simulating NAS)
