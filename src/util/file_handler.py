"""
File handling utilities for uploads and downloads
"""
import os
import uuid
from werkzeug.utils import secure_filename

class FileHandler:
    """Handle file uploads, downloads, and storage"""
    
    # Get project root directory (parent of src/)
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'uploads')
    OUTPUT_FOLDER = os.path.join(PROJECT_ROOT, 'outputs')
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 10MB
    
    @staticmethod
    def allowed_file(filename, allowed_extensions):
        """
        Check if file extension is allowed
        
        Args:
            filename (str): Name of the file
            allowed_extensions (list): List of allowed extensions
        
        Returns:
            bool: True if allowed, False otherwise
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    @staticmethod
    def save_upload(file, allowed_extensions):
        """
        Save uploaded file with unique name
        
        Args:
            file: FileStorage object from Flask request
            allowed_extensions (list): List of allowed extensions
        
        Returns:
            tuple: (file_path, original_filename, file_extension)
        
        Raises:
            ValueError: If file is not allowed or too large
        """
        if not file:
            raise ValueError("No file provided")
        
        if file.filename == '':
            raise ValueError("Empty filename")
        
        if not FileHandler.allowed_file(file.filename, allowed_extensions):
            raise ValueError(f"File type not allowed. Allowed: {', '.join(allowed_extensions)}")
        
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Ensure upload directory exists
        os.makedirs(FileHandler.UPLOAD_FOLDER, exist_ok=True)
        
        # Save file
        file_path = os.path.join(FileHandler.UPLOAD_FOLDER, unique_filename)
        file.save(file_path)
        
        # Check file size
        if os.path.getsize(file_path) > FileHandler.MAX_FILE_SIZE:
            os.remove(file_path)
            raise ValueError(f"File too large. Max size: {FileHandler.MAX_FILE_SIZE / 1024 / 1024}MB")
        
        return file_path, original_filename, file_extension
    
    @staticmethod
    def get_output_path(original_filename, output_extension):
        """
        Generate output file path
        
        Args:
            original_filename (str): Original filename
            output_extension (str): Desired output extension
        
        Returns:
            str: Path to output file
        """
        # Ensure output directory exists
        os.makedirs(FileHandler.OUTPUT_FOLDER, exist_ok=True)
        
        # Generate unique output filename
        base_name = os.path.splitext(secure_filename(original_filename))[0]
        unique_filename = f"{base_name}_{uuid.uuid4()}.{output_extension}"
        
        return os.path.join(FileHandler.OUTPUT_FOLDER, unique_filename)
    
    @staticmethod
    def cleanup_file(file_path):
        """
        Delete a file if it exists
        
        Args:
            file_path (str): Path to file to delete
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up file {file_path}: {e}")
    
    @staticmethod
    def get_file_size(file_path):
        """
        Get file size in bytes
        
        Args:
            file_path (str): Path to file
        
        Returns:
            int: File size in bytes
        """
        return os.path.getsize(file_path) if os.path.exists(file_path) else 0
