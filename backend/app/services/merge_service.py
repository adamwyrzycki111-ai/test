"""
PDF Merge Service using pypdf
Merges module PDFs and adds TOC, bookmarks, and page numbers
"""

import os
from datetime import datetime
from typing import List, Tuple
from pypdf import PdfReader, PdfWriter, PageObject
from pypdf.generic import Destination


class MergeService:
    """Service for merging PDFs and adding post-processing"""
    
    def __init__(self):
        self.page_number_font_size = 10
    
    def merge_pdfs(
        self,
        files_with_titles: List[Tuple[str, str]],
        work_order_number: str
    ) -> str:
        """
        Merge multiple PDFs into a single COC document.
        
        Args:
            files_with_titles: List of (file_path, title) tuples in merge order
            work_order_number: The work order number for the output filename
            
        Returns:
            Path to the merged PDF file
        """
        if not files_with_titles:
            raise ValueError("No files to merge")
        
        # Ensure all files exist
        for file_path, title in files_with_titles:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        # Create output path
        output_folder = document_service.get_final_folder()
        output_path = f"{output_folder}/{work_order_number}_COC.pdf"
        
        # Merge PDFs
        writer = PdfWriter()
        
        # Track page numbers for TOC
        page_offsets = []
        current_page = 0
        
        for file_path, title in files_with_titles:
            # Read the source PDF
            reader = PdfReader(file_path)
            page_offsets.append((current_page, title))
            
            # Add each page
            for page in reader.pages:
                writer.add_page(page)
                current_page += 1
        
        # Add TOC page at the beginning
        toc_page = self._create_toc_page(page_offsets)
        writer.insert_page(toc_page, 0)
        
        # Update page offsets after TOC insertion
        page_offsets = [(offset + 1, title) for offset, title in page_offsets]
        
        # Add page numbers to all pages
        self._add_page_numbers(writer)
        
        # Add bookmarks/outlines
        self._add_bookmarks(writer, page_offsets)
        
        # Write the final PDF
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        return output_path
    
    def _create_toc_page(self, page_offsets: List[Tuple[int, str]]) -> PageObject:
        """Create a Table of Contents page"""
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.lib.enums import TA_LEFT
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.styles import ParagraphStyle
        
        # Create TOC in a temporary file
        from io import BytesIO
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        elements = []
        
        # Title
        style = ParagraphStyle(
            'TOCTitle',
            fontSize=18,
            textColor=colors.HexColor("#1a1a1a"),
            spaceAfter=20,
            alignment=1,  # Center
        )
        elements.append(Paragraph("TABLE OF CONTENTS", style))
        elements.append(Spacer(1, 30))
        
        # TOC entries
        toc_data = [['Section', 'Page']]
        for page_num, title in page_offsets:
            toc_data.append([title, str(page_num)])
        
        table = Table(toc_data, colWidths=[4*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1a1a1a")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(table)
        
        doc.build(elements)
        buffer.seek(0)
        
        # Read the generated TOC PDF
        reader = PdfReader(buffer)
        toc_page = reader.pages[0]
        
        return toc_page
    
    def _add_page_numbers(self, writer: PdfWriter) -> None:
        """Add page numbers to all pages"""
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from io import BytesIO
        
        total_pages = len(writer.pages)
        
        for i in range(total_pages):
            # Create a transparent page number overlay
            packet = BytesIO()
            c = canvas.Canvas(packet, pagesize=A4)
            
            # Page number at bottom center
            page_num = i + 1
            c.setFont("Helvetica", 10)
            c.setFillColorRGB(0.3, 0.3, 0.3)
            c.drawString(300, 20, f"Page {page_num} of {total_pages}")
            
            c.save()
            packet.seek(0)
            
            # Merge the page number onto the existing page
            from pypdf import PdfReader
            number_reader = PdfReader(packet)
            number_page = number_reader.pages[0]
            
            # Get the current page and merge
            current_page = writer.pages[i]
            current_page.merge_page(number_page)
    
    def _add_bookmarks(self, writer: PdfWriter, section_pages: List[Tuple[int, str]]) -> None:
        """Add bookmarks/outlines to the PDF"""
        from pypdf.generic import Destination, ArrayObject
        
        # Create outline (bookmarks)
        outline = writer.add_outline_item("Certificate of Conformance", 0)
        
        for page_num, title in section_pages:
            writer.add_outline_item(title, page_num, parent=outline)


# Import document service for paths
from .document_service import document_service


# Singleton instance
merge_service = MergeService()