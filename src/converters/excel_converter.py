"""
Excel Converter Module
Supports PDF to Excel and Excel to PDF conversions
"""
import os
import tabula
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors


class ExcelConverter:
    """Handle Excel and PDF conversions"""
    
    SUPPORTED_FORMATS = ['xlsx', 'xls', 'pdf']
    
    def __init__(self):
        """Initialize the Excel converter"""
        pass
    
    @staticmethod
    def is_supported(format_name):
        """Check if format is supported"""
        return format_name.lower() in ExcelConverter.SUPPORTED_FORMATS
    
    @staticmethod
    def pdf_to_excel(pdf_path, excel_path):
        """
        Convert PDF to Excel by extracting tables
        
        Args:
            pdf_path (str): Path to input PDF file
            excel_path (str): Path to save Excel file
        
        Returns:
            str: Path to converted file
        
        Raises:
            FileNotFoundError: If input file doesn't exist
            Exception: If conversion fails
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        try:
            # Extract tables from PDF using tabula
            # pages='all' extracts from all pages
            # multiple_tables=True returns list of DataFrames
            tables = tabula.read_pdf(
                pdf_path,
                pages='all',
                multiple_tables=True,
                lattice=True  # Use lattice mode for better table detection
            )
            
            if not tables or len(tables) == 0:
                # If no tables found with lattice, try stream mode
                tables = tabula.read_pdf(
                    pdf_path,
                    pages='all',
                    multiple_tables=True,
                    stream=True
                )
            
            if not tables or len(tables) == 0:
                raise Exception("No tables found in PDF. The PDF may not contain tabular data.")
            
            # Create Excel writer
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                # Write each table to a separate sheet
                for idx, table in enumerate(tables):
                    if not table.empty:
                        sheet_name = f'Table_{idx + 1}'
                        # Limit sheet name to 31 characters (Excel limit)
                        sheet_name = sheet_name[:31]
                        table.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Format the Excel file
            ExcelConverter._format_excel(excel_path)
            
            return excel_path
            
        except Exception as e:
            raise Exception(f"PDF to Excel conversion failed: {str(e)}")
    
    @staticmethod
    def _format_excel(excel_path):
        """
        Apply basic formatting to Excel file
        
        Args:
            excel_path (str): Path to Excel file to format
        """
        try:
            wb = load_workbook(excel_path)
            
            for sheet in wb.worksheets:
                # Format header row
                for cell in sheet[1]:
                    cell.font = Font(bold=True)
                    cell.alignment = Alignment(horizontal='center', vertical='center')
                
                # Auto-adjust column widths
                for column in sheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    
                    for cell in column:
                        try:
                            if cell.value:
                                max_length = max(max_length, len(str(cell.value)))
                        except:
                            pass
                    
                    adjusted_width = min(max_length + 2, 50)  # Cap at 50
                    sheet.column_dimensions[column_letter].width = adjusted_width
            
            wb.save(excel_path)
        except Exception as e:
            # If formatting fails, just continue with unformatted file
            pass
    
    @staticmethod
    def excel_to_pdf(excel_path, pdf_path):
        """
        Convert Excel to PDF
        
        Args:
            excel_path (str): Path to input Excel file
            pdf_path (str): Path to save PDF file
        
        Returns:
            str: Path to converted file
        
        Raises:
            FileNotFoundError: If input file doesn't exist
            Exception: If conversion fails
        """
        if not os.path.exists(excel_path):
            raise FileNotFoundError(f"Excel file not found: {excel_path}")
        
        try:
            # Read Excel file
            excel_file = pd.ExcelFile(excel_path)
            
            # Create PDF
            pdf_doc = SimpleDocTemplate(
                pdf_path,
                pagesize=A4,
                rightMargin=30,
                leftMargin=30,
                topMargin=30,
                bottomMargin=30
            )
            
            styles = getSampleStyleSheet()
            story = []
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=14,
                spaceAfter=12,
                textColor=colors.HexColor('#1a1a1a')
            )
            
            # Process each sheet
            for sheet_idx, sheet_name in enumerate(excel_file.sheet_names):
                # Read sheet data
                df = pd.read_excel(excel_path, sheet_name=sheet_name)
                
                # Add sheet title
                if len(excel_file.sheet_names) > 1:
                    story.append(Paragraph(f"Sheet: {sheet_name}", title_style))
                    story.append(Spacer(1, 0.2 * inch))
                
                # Convert DataFrame to list of lists for ReportLab Table
                data = [df.columns.tolist()] + df.values.tolist()
                
                # Convert all values to strings and handle NaN
                data = [[str(cell) if pd.notna(cell) else '' for cell in row] for row in data]
                
                # Create table
                table = Table(data)
                
                # Style the table
                table_style = TableStyle([
                    # Header row
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    
                    # Data rows
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    
                    # Grid
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('BOX', (0, 0), (-1, -1), 1, colors.black),
                    
                    # Alternating row colors
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ])
                
                table.setStyle(table_style)
                story.append(table)
                
                # Add page break between sheets (except for last sheet)
                if sheet_idx < len(excel_file.sheet_names) - 1:
                    story.append(PageBreak())
            
            # Build PDF
            pdf_doc.build(story)
            
            return pdf_path
            
        except Exception as e:
            raise Exception(f"Excel to PDF conversion failed: {str(e)}")
    
    @staticmethod
    def convert(input_path, output_path, input_format, output_format):
        """
        Convert between Excel and PDF formats
        
        Args:
            input_path (str): Path to input file
            output_path (str): Path to save converted file
            input_format (str): Input format (pdf or xlsx/xls)
            output_format (str): Output format (pdf or xlsx/xls)
        
        Returns:
            str: Path to converted file
        
        Raises:
            ValueError: If conversion not supported
        """
        input_format = input_format.lower()
        output_format = output_format.lower()
        
        if not ExcelConverter.is_supported(input_format):
            raise ValueError(f"Unsupported input format: {input_format}")
        
        if not ExcelConverter.is_supported(output_format):
            raise ValueError(f"Unsupported output format: {output_format}")
        
        if input_format == output_format:
            raise ValueError("Input and output formats are the same")
        
        # Route to appropriate converter
        if input_format == 'pdf' and output_format in ['xlsx', 'xls']:
            return ExcelConverter.pdf_to_excel(input_path, output_path)
        elif input_format in ['xlsx', 'xls'] and output_format == 'pdf':
            return ExcelConverter.excel_to_pdf(input_path, output_path)
        else:
            raise ValueError(f"Conversion from {input_format} to {output_format} not supported")
    
    @staticmethod
    def get_excel_info(file_path):
        """
        Get information about an Excel file
        
        Args:
            file_path (str): Path to Excel file
        
        Returns:
            dict: Excel file information
        """
        try:
            excel_file = pd.ExcelFile(file_path)
            
            info = {
                'format': 'xlsx' if file_path.endswith('.xlsx') else 'xls',
                'size': os.path.getsize(file_path),
                'sheets': excel_file.sheet_names,
                'sheet_count': len(excel_file.sheet_names)
            }
            
            return info
        except Exception as e:
            return {
                'format': 'unknown',
                'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0,
                'error': str(e)
            }
