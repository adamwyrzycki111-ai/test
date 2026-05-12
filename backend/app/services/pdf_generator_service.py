"""
PDF Generation Service using ReportLab
Generates module PDFs for the COC system
"""

import os
from datetime import datetime
from typing import List
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from ..models import WorkOrder, ElectricalTestItem, MechanicalTestItem, FaiFormItem
from .document_service import document_service


class PdfGeneratorService:
    """Service for generating module PDFs"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom styles for industrial look"""
        # Title style - bold industrial
        self.styles.add(ParagraphStyle(
            name='IndustrialTitle',
            parent=self.styles['Title'],
            fontSize=18,
            textColor=colors.HexColor("#1a1a1a"),
            spaceAfter=20,
            alignment=TA_CENTER
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor("#2d2d2d"),
            spaceAfter=10,
            spaceBefore=15
        ))
        
        # Info label style
        self.styles.add(ParagraphStyle(
            name='InfoLabel',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor("#5a5a5a"),
            spaceAfter=3
        ))
        
        # Info value style
        self.styles.add(ParagraphStyle(
            name='InfoValue',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor("#1a1a1a"),
            spaceAfter=10
        ))
    
    def _create_header_section(self, work_order: WorkOrder) -> List:
        """Create the header section with work order info"""
        elements = []
        
        # Title
        elements.append(Paragraph("QUALITY INSPECTION REPORT", self.styles['IndustrialTitle']))
        elements.append(Spacer(1, 10))
        
        # Work order info table
        info_data = [
            ['Work Order:', work_order.work_order_number, 'Part Number:', work_order.part_number],
            ['Lot Number:', work_order.lot_number, 'Customer:', work_order.customer]
        ]
        
        info_table = Table(info_data, colWidths=[1.2*inch, 2*inch, 1.2*inch, 2*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor("#5a5a5a")),
            ('TEXTCOLOR', (2, 0), (2, -1), colors.HexColor("#5a5a5a")),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor("#1a1a1a")),
            ('TEXTCOLOR', (3, 0), (3, -1), colors.HexColor("#1a1a1a")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_inspector_footer(self, inspector: str) -> List:
        """Create the inspector signature section"""
        elements = []
        elements.append(Spacer(1, 30))
        
        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Inspector info table
        footer_data = [
            ['Inspector:', inspector, 'Date:', timestamp]
        ]
        
        footer_table = Table(footer_data, colWidths=[1*inch, 2.5*inch, 1*inch, 2.5*inch])
        footer_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#5a5a5a")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        elements.append(footer_table)
        
        # Signature placeholder
        elements.append(Spacer(1, 30))
        signature_data = [['Signature:']]
        signature_table = Table(signature_data, colWidths=[3*inch])
        signature_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#5a5a5a")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
        ]))
        elements.append(signature_table)
        
        return elements
    
    def generate_electrical_test_pdf(
        self,
        work_order: WorkOrder,
        inspector: str = "J. Martinez",
        items: List[ElectricalTestItem] = None
    ) -> str:
        """Generate Electrical Test PDF"""
        
        # Default test data
        if items is None:
            items = [
                ElectricalTestItem(test="Insulation Resistance", spec=">100MΩ", result="147MΩ", status="PASS"),
                ElectricalTestItem(test="Dielectric Strength", spec="1500VAC", result="1520VAC", status="PASS"),
                ElectricalTestItem(test="Continuity", spec="<0.1Ω", result="0.042Ω", status="PASS"),
                ElectricalTestItem(test="Ground Continuity", spec="<0.5Ω", result="0.18Ω", status="PASS"),
                ElectricalTestItem(test="Hipot Test", spec="1500VAC/1min", result="PASS", status="PASS"),
            ]
        
        # Get file path
        folder = document_service.get_document_folder(work_order.work_order_number)
        file_path = f"{folder}/electrical_test.pdf"
        
        # Create PDF
        doc = SimpleDocTemplate(
            file_path,
            pagesize=A4,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Build content
        elements = []
        
        # Header
        elements.extend(self._create_header_section(work_order))
        
        # Document title
        elements.append(Paragraph("ELECTRICAL TEST REPORT", self.styles['SectionHeader']))
        elements.append(Spacer(1, 10))
        
        # Test results table
        table_data = [['Test', 'Specification', 'Result', 'Status']]
        for item in items:
            table_data.append([item.test, item.spec, item.result, item.status])
        
        table = Table(table_data, colWidths=[2.5*inch, 1.5*inch, 1.25*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2d5016")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#1a1a1a")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
        ]))
        
        elements.append(table)
        
        # Footer
        elements.extend(self._create_inspector_footer(inspector))
        
        # Build PDF
        doc.build(elements)
        
        return file_path
    
    def generate_mechanical_test_pdf(
        self,
        work_order: WorkOrder,
        inspector: str = "R. Thompson",
        items: List[MechanicalTestItem] = None
    ) -> str:
        """Generate Mechanical Test PDF"""
        
        # Default test data
        if items is None:
            items = [
                MechanicalTestItem(test="Dimensional Check", spec="±0.05mm", result="+0.02mm", status="PASS"),
                MechanicalTestItem(test="Torque Test", spec="15-20 Nm", result="17.5 Nm", status="PASS"),
                MechanicalTestItem(test="Thread Inspection", spec="No defects", result="No defects found", status="PASS"),
                MechanicalTestItem(test="Visual Inspection", spec="Per ASME", result="Compliant", status="PASS"),
                MechanicalTestItem(test="Hardness Test", spec="55-65 HRC", result="58 HRC", status="PASS"),
            ]
        
        # Get file path
        folder = document_service.get_document_folder(work_order.work_order_number)
        file_path = f"{folder}/mechanical_test.pdf"
        
        # Create PDF
        doc = SimpleDocTemplate(
            file_path,
            pagesize=A4,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Build content
        elements = []
        
        # Header
        elements.extend(self._create_header_section(work_order))
        
        # Document title
        elements.append(Paragraph("MECHANICAL TEST REPORT", self.styles['SectionHeader']))
        elements.append(Spacer(1, 10))
        
        # Test results table
        table_data = [['Test', 'Specification', 'Result', 'Status']]
        for item in items:
            table_data.append([item.test, item.spec, item.result, item.status])
        
        table = Table(table_data, colWidths=[2.5*inch, 1.5*inch, 1.25*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#162d5c")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#1a1a1a")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f5ff")]),
        ]))
        
        elements.append(table)
        
        # Footer
        elements.extend(self._create_inspector_footer(inspector))
        
        # Build PDF
        doc.build(elements)
        
        return file_path
    
    def generate_fai_form_pdf(
        self,
        work_order: WorkOrder,
        inspector: str = "K. Williams",
        items: List[FaiFormItem] = None
    ) -> str:
        """Generate FAI Form PDF"""
        
        # Default FAI data
        if items is None:
            items = [
                FaiFormItem(item="1", description="Main Body Assembly", spec="Per drawing", actual="Conforms", status="APPROVED"),
                FaiFormItem(item="2", description="Mounting Brackets", spec="Per drawing", actual="Conforms", status="APPROVED"),
                FaiFormItem(item="3", description="Fasteners", spec="Per spec", actual="Conforms", status="APPROVED"),
                FaiFormItem(item="4", description="Seals", spec="Per spec", actual="Conforms", status="APPROVED"),
                FaiFormItem(item="5", description="Finish", spec="Per MIL-PRF", actual="Conforms", status="APPROVED"),
                FaiFormItem(item="6", description="Marking", spec="Per spec", actual="Conforms", status="APPROVED"),
            ]
        
        # Get file path
        folder = document_service.get_document_folder(work_order.work_order_number)
        file_path = f"{folder}/fai_form.pdf"
        
        # Create PDF
        doc = SimpleDocTemplate(
            file_path,
            pagesize=A4,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Build content
        elements = []
        
        # Header
        elements.extend(self._create_header_section(work_order))
        
        # Document title
        elements.append(Paragraph("FIRST ARTICLE INSPECTION (FAI) FORM", self.styles['SectionHeader']))
        elements.append(Spacer(1, 10))
        
        # FAI items table
        table_data = [['Item', 'Description', 'Specification', 'Actual', 'Status']]
        for item in items:
            table_data.append([item.item, item.description, item.spec, item.actual, item.status])
        
        table = Table(table_data, colWidths=[0.5*inch, 2*inch, 1.5*inch, 1.25*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#5c3a16")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (-1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#1a1a1a")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#fff5f0")]),
        ]))
        
        elements.append(table)
        
        # Footer
        elements.extend(self._create_inspector_footer(inspector))
        
        # Build PDF
        doc.build(elements)
        
        return file_path


# Singleton instance
pdf_generator_service = PdfGeneratorService()