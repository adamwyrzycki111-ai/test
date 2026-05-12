# Quality Inspection & Certificate of Conformance (COC) System - MVP Specification

## 1. Project Overview

**Project Name:** COC Inspector
**Type:** Industrial Quality Inspection & Certificate of Conformance (COC) Web Application
**Core Functionality:** A technical proof-of-concept demonstrating document orchestration, PDF generation, merge pipeline, and workflow validation for manufacturing compliance.
**Target Users:** QA inspectors, quality engineers, and compliance officers in aerospace/manufacturing industries.

---

## 2. UI/UX Specification

### Layout Structure

**Page Sections:**
- **Header:** App title, industrial-style branding
- **Main Content Area:** Work Order selection → Document configuration → PDF generation → Validation → Merge → Download
- **Footer:** Minimal, version info only

**Grid/Flex Layout:**
- CSS Flexbox for main layout
- CSS Grid for document cards (2-column on desktop, 1-column on mobile)

**Responsive Breakpoints:**
- Mobile: 0-768px (single column)
- Tablet: 769-1024px (adjusted spacing)
- Desktop: 1025px+ (full layout)

### Visual Design

**Color Palette:**
- Background: #0a0f14 (deep industrial black)
- Surface: #151c24 (dark steel)
- Surface Secondary: #1e2731 (lighter steel)
- Border: #2a3542 (steel border)
- Primary: #ff6b35 (industrial orange)
- Primary Hover: #ff8555
- Secondary: #3d8bfd (technical blue)
- Success: #22c55e (verified green)
- Warning: #f59e0b (attention amber)
- Error: #ef4444 (blocked red)
- Text Primary: #e8edf4 (bright steel)
- Text Secondary: #8b98a8 (muted steel)
- Text Muted: #5a6572 (dim)

**Typography:**
- Font Family: "JetBrains Mono", "Fira Code", monospace (industrial/technical feel)
- Headings: JetBrains Mono Bold
- Body: JetBrains Mono Regular
- Font Sizes:
  - H1: 28px
  - H2: 22px
  - H3: 18px
  - Body: 14px
  - Small: 12px

**Spacing System:**
- Base unit: 4px
- Component padding: 16px
- Card padding: 20px
- Section gap: 32px
- Element gap: 12px

**Visual Effects:**
- No rounded corners (sharp, industrial)
- Subtle border-based elevation (no shadows)
- Status indicators with color-coded left borders
- Terminal-style input fields with monospace font

### Components

**1. Header Bar**
- Full-width dark bar
- App title left-aligned
- Status indicator right

**2. Work Order Panel**
- Display: Work Order Number, Part Number, Lot Number, Customer
- Mock data with industrial aesthetic

**3. Document Card**
- States: Missing (red border), Generated (green), Uploaded (blue), Ready (orange)
- Each card has: document name, type badge, status, action button
- Document type badges: "Generated" | "Uploaded" | "System"

**4. Action Buttons**
- Primary: Orange background, dark text
- Secondary: Outlined with border
- Disabled: Grayed out
- Hover: Slight background change

**5. Status Badges**
- Small pill-shaped badges with color coding
- States: Missing, Generated, Uploaded, Ready, Blocked

**6. Validation Error Panel**
- Red border panel
- List of missing documents
- Blocked state indicator

**7. Merge Progress Indicator**
- Step-based progress: Validate → Merge → Post-process → Complete
- Visual step indicators

**8. Download Button**
- Prominent final action button
- Green when ready, disabled when not

---

## 3. Functionality Specification

### Core Features

**1. Work Order Management**
- Pre-loaded mock work orders
- Selection UI to switch between orders
- Display: WO#, Part#, Lot#, Customer

**2. Document Configuration**
- Required document checklist
- Configurable document types:
  - Electrical Test (generated)
  - Mechanical Test (generated)
  - FAI Form (generated)
  - External Lab Report (uploaded)

**3. Module PDF Generation**
- Individual "Generate" buttons per document
- Uses QuestPDF to create structured PDFs
- Each PDF contains:
  - Document title
  - Work order info (WO#, Part#, Lot#, Customer)
  - Table data (test results/sections)
  - Inspector name
  - Timestamp
  - Signature placeholder
- Saves to: /storage/nas/generated/{work_order}/{document_name}.pdf

**4. External PDF Upload**
- File upload interface
- Accepts PDF files only
- Saves to: /storage/nas/generated/{work_order}/external_{filename}.pdf
- Marks document as "Uploaded"

**5. Validation Logic**
- Validates all required documents exist before merge
- Checklist for each required document type
- Blocks merge if any document missing
- Shows clear error message listing missing docs

**6. Final Merge Engine**
- Uses iText7 for PDF merge
- Merge order from configuration array
- Preserves document order:
  1. Electrical Test
  2. Mechanical Test
  3. FAI Form
  4. External Lab Report

**7. Post-Processing**
- Add page numbers to all pages
- Add bookmarks for each section
- Generate Table of Contents page
- Create final merged PDF

**8. Final Output**
- Save to: /storage/nas/final/{work_order}_COC.pdf
- Download link in UI

### User Interactions and Flows

**Main Flow:**
1. User views Work Order screen
2. Selects Work Order (or uses default)
3. Views Required Documents checklist
4. Generates each module PDF (one by one)
5. Uploads External Lab Report PDF
6. System validates all docs present
7. Clicks "Generate Final COC"
8. System merges and post-processes
9. Download button becomes enabled

### Edge Cases
- No work order selected → show prompt
- Document generation fails → show error
- Upload non-PDF → reject with message
- Missing documents → block merge, show error
- Merge already exists → confirm overwrite

---

## 4. Acceptance Criteria

### Visual Checkpoints
- [ ] Industrial dark theme applied
- [ ] Monospace fonts throughout
- [ ] Sharp corners on all elements (no border-radius)
- [ ] Status colors visible on document cards
- [ ] Orange primary color on main buttons

### Functional Checkpoints
- [ ] Work order displays mock data
- [ ] All four document types visible
- [ ] Generate PDF creates file in NAS folder
- [ ] Upload PDF stores file in NAS folder
- [ ] Validation shows error for missing docs
- [ ] Merge button disabled when docs missing
- [ ] Merge creates combined PDF
- [ ] Final PDF has page numbers
- [ ] Download provides final PDF file

### Success Conditions
1. Complete workflow runs end-to-end
2. All document types can be generated
3. External PDF upload works
4. Validation correctly blocks on missing docs
5. Final merged PDF is downloadable
6. Architecture shows clear separation of concerns

---

## 5. Technical Architecture

### Backend Services Structure
```
/backend/
├── Controllers/
│   └── CocController.cs
├── Services/
│   ├── WorkOrderService.cs
│   ├── DocumentService.cs
│   ├── ValidationService.cs
│   └── MergeService.cs
├── PdfGeneration/
│   ├── ElectricalTestPdf.cs
│   ├── MechanicalTestPdf.cs
│   └── FaiFormPdf.cs
├── Models/
│   ├── WorkOrder.cs
│   └── Document.cs
└── Program.cs
```

### Frontend Structure
```
/frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── types/
│   └── App.tsx
└── package.json
```

### NAS Storage Structure
```
/storage/
└── nas/
    ├── generated/
    │   └── {work_order}/
    │       ├── electrical_test.pdf
    │       ├── mechanical_test.pdf
    │       ├── fai_form.pdf
    │       └── external_*.pdf
    └── final/
        └── {work_order}_COC.pdf
```

---

## 6. Mock Data

### Work Order
```json
{
  "workOrderNumber": "WO-2024-001847",
  "partNumber": "PN-AS-8847-A",
  "lotNumber": "LOT-2024-0347",
  "customer": "AeroSpace Dynamics Inc."
}
```

### Required Documents
```json
[
  { "id": "electrical_test", "name": "Electrical Test", "type": "generated" },
  { "id": "mechanical_test", "name": "Mechanical Test", "type": "generated" },
  { "id": "fai_form", "name": "FAI Form", "type": "generated" },
  { "id": "external_lab", "name": "External Lab Report", "type": "uploaded" }
]
```

### PDF Test Data
```json
{
  "electrical_test": {
    "title": "Electrical Test Report",
    "inspector": "J. Martinez",
    "items": [
      { "test": "Insulation Resistance", "spec": ">100MΩ", "result": "147MΩ", "status": "PASS" },
      { "test": "Dielectric Strength", "spec": "1500VAC", "result": "1520VAC", "status": "PASS" },
      { "test": "Continuity", "spec": "<0.1Ω", "result": "0.042Ω", "status": "PASS" }
    ]
  }
}
```