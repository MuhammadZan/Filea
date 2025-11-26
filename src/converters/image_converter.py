"""
Image Converter Module
Supports conversion between various image formats including AVIF
"""
import os
from PIL import Image
import pillow_avif

class ImageConverter:
    """Handle image format conversions"""
    
    SUPPORTED_FORMATS = ['png', 'jpg', 'jpeg', 'webp', 'bmp', 'gif', 'avif']
    
    def __init__(self):
        """Initialize the image converter"""
        pass
    
    @staticmethod
    def is_supported(format_name):
        """Check if format is supported"""
        return format_name.lower() in ImageConverter.SUPPORTED_FORMATS
    
    @staticmethod
    def convert(input_path, output_path, output_format):
        """
        Convert image from one format to another
        
        Args:
            input_path (str): Path to input image
            output_path (str): Path to save converted image
            output_format (str): Target format (png, jpg, webp, avif, etc.)
        
        Returns:
            str: Path to converted file
        
        Raises:
            ValueError: If format is not supported
            FileNotFoundError: If input file doesn't exist
        """
        output_format = output_format.lower()
        
        if not ImageConverter.is_supported(output_format):
            raise ValueError(f"Unsupported output format: {output_format}")
        
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Open the image
        with Image.open(input_path) as img:
            # Convert RGBA to RGB for formats that don't support transparency
            if output_format in ['jpg', 'jpeg'] and img.mode in ['RGBA', 'LA', 'P']:
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Handle JPEG format
            save_format = 'JPEG' if output_format in ['jpg', 'jpeg'] else output_format.upper()
            
            # Save with appropriate quality settings
            save_kwargs = {}
            if output_format in ['jpg', 'jpeg']:
                save_kwargs['quality'] = 95
                save_kwargs['optimize'] = True
            elif output_format == 'png':
                save_kwargs['optimize'] = True
            elif output_format == 'webp':
                save_kwargs['quality'] = 95
            elif output_format == 'avif':
                save_kwargs['quality'] = 90
            
            # Save the converted image
            img.save(output_path, format=save_format, **save_kwargs)
        
        return output_path
    
    @staticmethod
    def get_image_info(file_path):
        """
        Get information about an image file
        
        Args:
            file_path (str): Path to image file
        
        Returns:
            dict: Image information (format, size, mode)
        """
        with Image.open(file_path) as img:
            return {
                'format': img.format,
                'size': img.size,
                'mode': img.mode,
                'width': img.width,
                'height': img.height
            }
