"""
Conversion API Routes
Handles file conversion endpoints
"""
from flask import Blueprint, request, send_file, jsonify
from flask.ext.restful import Api, Resource
import os

from converters.image_converter import ImageConverter
from util.file_handler import FileHandler

conversion_blueprint = Blueprint('conversion', __name__)
conversion_blueprint_api = Api(conversion_blueprint)


class ImageConversionAPI(Resource):
    """Handle image format conversions"""
    
    def post(self):
        """
        Convert image from one format to another
        
        Request:
            - file: Image file (multipart/form-data)
            - to_format: Target format (png, jpg, webp, avif, etc.)
        
        Returns:
            Converted image file
        """
        try:
            # Check if file is present
            if 'file' not in request.files:
                return {'error': 'No file provided'}, 400
            
            file = request.files['file']
            to_format = request.form.get('to_format', '').lower()
            
            if not to_format:
                return {'error': 'to_format parameter required'}, 400
            
            # Validate output format
            if not ImageConverter.is_supported(to_format):
                return {
                    'error': f'Unsupported format: {to_format}',
                    'supported_formats': ImageConverter.SUPPORTED_FORMATS
                }, 400
            
            # Save uploaded file
            input_path, original_filename, input_ext = FileHandler.save_upload(
                file, 
                ImageConverter.SUPPORTED_FORMATS
            )
            
            # Generate output path
            output_path = FileHandler.get_output_path(original_filename, to_format)
            
            try:
                # Convert the image
                ImageConverter.convert(input_path, output_path, to_format)
                
                # Send the converted file
                response = send_file(
                    output_path,
                    as_attachment=True,
                    attachment_filename=f"{os.path.splitext(original_filename)[0]}.{to_format}"
                )
                
                # Clean up files after sending
                @response.call_on_close
                def cleanup():
                    FileHandler.cleanup_file(input_path)
                    FileHandler.cleanup_file(output_path)
                
                return response
                
            except Exception as e:
                # Clean up on error
                FileHandler.cleanup_file(input_path)
                FileHandler.cleanup_file(output_path)
                raise e
                
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'Conversion failed: {str(e)}'}, 500


class SupportedFormatsAPI(Resource):
    """List all supported formats"""
    
    def get(self):
        """Get list of supported formats by category"""
        return {
            'images': ImageConverter.SUPPORTED_FORMATS,
            'documents': ['pdf', 'docx'],
            'spreadsheets': ['xlsx', 'xls', 'pdf']  # Excel and PDF
        }


class PDFToWordAPI(Resource):
    """Convert PDF to Word"""
    
    def post(self):
        """
        Convert PDF to Word document
        
        Request:
            - file: PDF file (multipart/form-data)
        
        Returns:
            Converted Word document
        """
        try:
            from converters.pdf_converter import DocumentConverter
            
            # Check if file is present
            if 'file' not in request.files:
                return {'error': 'No file provided'}, 400
            
            file = request.files['file']
            
            # Save uploaded file
            input_path, original_filename, input_ext = FileHandler.save_upload(
                file, 
                ['pdf']
            )
            
            # Generate output path
            output_path = FileHandler.get_output_path(original_filename, 'docx')
            
            try:
                # Convert PDF to Word
                DocumentConverter.pdf_to_word(input_path, output_path)
                
                # Send the converted file
                response = send_file(
                    output_path,
                    as_attachment=True,
                    attachment_filename=f"{os.path.splitext(original_filename)[0]}.docx"
                )
                
                # Clean up files after sending
                @response.call_on_close
                def cleanup():
                    FileHandler.cleanup_file(input_path)
                    FileHandler.cleanup_file(output_path)
                
                return response
                
            except Exception as e:
                # Clean up on error
                FileHandler.cleanup_file(input_path)
                FileHandler.cleanup_file(output_path)
                raise e
                
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'Conversion failed: {str(e)}'}, 500


class WordToPDFAPI(Resource):
    """Convert Word to PDF"""
    
    def post(self):
        """
        Convert Word document to PDF
        
        Request:
            - file: Word file (multipart/form-data)
        
        Returns:
            Converted PDF document
        """
        try:
            from converters.pdf_converter import DocumentConverter
            
            # Check if file is present
            if 'file' not in request.files:
                return {'error': 'No file provided'}, 400
            
            file = request.files['file']
            
            # Save uploaded file
            input_path, original_filename, input_ext = FileHandler.save_upload(
                file, 
                ['docx', 'doc']
            )
            
            # Generate output path
            output_path = FileHandler.get_output_path(original_filename, 'pdf')
            
            try:
                # Convert Word to PDF
                DocumentConverter.word_to_pdf(input_path, output_path)
                
                # Send the converted file
                response = send_file(
                    output_path,
                    as_attachment=True,
                    attachment_filename=f"{os.path.splitext(original_filename)[0]}.pdf"
                )
                
                # Clean up files after sending
                @response.call_on_close
                def cleanup():
                    FileHandler.cleanup_file(input_path)
                    FileHandler.cleanup_file(output_path)
                
                return response
                
            except Exception as e:
                # Clean up on error
                FileHandler.cleanup_file(input_path)
                FileHandler.cleanup_file(output_path)
                raise e
                
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'Conversion failed: {str(e)}'}, 500


class PDFToExcelAPI(Resource):
    """Convert PDF to Excel"""
    
    def post(self):
        """
        Convert PDF to Excel spreadsheet
        
        Request:
            - file: PDF file (multipart/form-data)
        
        Returns:
            Converted Excel file (.xlsx)
        """
        try:
            from converters.excel_converter import ExcelConverter
            
            # Check if file is present
            if 'file' not in request.files:
                return {'error': 'No file provided'}, 400
            
            file = request.files['file']
            
            # Save uploaded file
            input_path, original_filename, input_ext = FileHandler.save_upload(
                file, 
                ['pdf']
            )
            
            # Generate output path
            output_path = FileHandler.get_output_path(original_filename, 'xlsx')
            
            try:
                # Convert PDF to Excel
                ExcelConverter.pdf_to_excel(input_path, output_path)
                
                # Send the converted file
                response = send_file(
                    output_path,
                    as_attachment=True,
                    attachment_filename=f"{os.path.splitext(original_filename)[0]}.xlsx"
                )
                
                # Clean up files after sending
                @response.call_on_close
                def cleanup():
                    FileHandler.cleanup_file(input_path)
                    FileHandler.cleanup_file(output_path)
                
                return response
                
            except Exception as e:
                # Clean up on error
                FileHandler.cleanup_file(input_path)
                FileHandler.cleanup_file(output_path)
                raise e
                
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'Conversion failed: {str(e)}'}, 500


class ExcelToPDFAPI(Resource):
    """Convert Excel to PDF"""
    
    def post(self):
        """
        Convert Excel spreadsheet to PDF
        
        Request:
            - file: Excel file (multipart/form-data)
        
        Returns:
            Converted PDF document
        """
        try:
            from converters.excel_converter import ExcelConverter
            
            # Check if file is present
            if 'file' not in request.files:
                return {'error': 'No file provided'}, 400
            
            file = request.files['file']
            
            # Save uploaded file
            input_path, original_filename, input_ext = FileHandler.save_upload(
                file, 
                ['xlsx', 'xls']
            )
            
            # Generate output path
            output_path = FileHandler.get_output_path(original_filename, 'pdf')
            
            try:
                # Convert Excel to PDF
                ExcelConverter.excel_to_pdf(input_path, output_path)
                
                # Send the converted file
                response = send_file(
                    output_path,
                    as_attachment=True,
                    attachment_filename=f"{os.path.splitext(original_filename)[0]}.pdf"
                )
                
                # Clean up files after sending
                @response.call_on_close
                def cleanup():
                    FileHandler.cleanup_file(input_path)
                    FileHandler.cleanup_file(output_path)
                
                return response
                
            except Exception as e:
                # Clean up on error
                FileHandler.cleanup_file(input_path)
                FileHandler.cleanup_file(output_path)
                raise e
                
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'Conversion failed: {str(e)}'}, 500


class HealthCheckAPI(Resource):
    """Health check endpoint"""
    
    def get(self):
        """Check if API is running"""
        return {
            'status': 'healthy',
            'service': 'File Conversion API',
            'version': '1.0.0'
        }



# Register endpoints
conversion_blueprint_api.add_resource(ImageConversionAPI, '/convert/image')
conversion_blueprint_api.add_resource(PDFToWordAPI, '/convert/pdf-to-word')
conversion_blueprint_api.add_resource(WordToPDFAPI, '/convert/word-to-pdf')
conversion_blueprint_api.add_resource(PDFToExcelAPI, '/convert/pdf-to-excel')
conversion_blueprint_api.add_resource(ExcelToPDFAPI, '/convert/excel-to-pdf')
conversion_blueprint_api.add_resource(SupportedFormatsAPI, '/formats')
conversion_blueprint_api.add_resource(HealthCheckAPI, '/health')
