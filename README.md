# File Conversion API

A Flask-based REST API for converting files between different formats without using paid services.

## Features

✅ **Image Conversion** - PNG, JPG, WEBP, BMP, GIF, AVIF  
✅ **Document Conversion** - PDF ↔ Word  
🚧 **Spreadsheet Conversion** - Excel → PDF (Coming in Phase 3)

## Quick Start

### 1. Setup Environment

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies (if not already installed)
pip install -r requirements.txt
```

### 2. Start Server

```bash
# Set environment variables and start
HOST=localhost PORT=5001 python src/server.py
```

> **Note**: Port 5000 is blocked by macOS AirPlay. Use port 5001 or configure in `.env`

### 3. Test API

```bash
# Health check
curl http://localhost:5001/api/health

# List supported formats
curl http://localhost:5001/api/formats
```

## API Endpoints

### Image Conversion

Convert images between formats:

```bash
POST /api/convert/image
```

**Parameters:**
- `file` - Image file (multipart/form-data)
- `to_format` - Target format: `png`, `jpg`, `webp`, `avif`, `bmp`, `gif`

**Example:**

```bash
# Convert PNG to WEBP
curl -X POST \
  -F "file=@photo.png" \
  -F "to_format=webp" \
  http://localhost:5001/api/convert/image \
  -o photo.webp

# Convert JPG to AVIF
curl -X POST \
  -F "file=@image.jpg" \
  -F "to_format=avif" \
  http://localhost:5001/api/convert/image \
  -o image.avif
```

### PDF to Word Conversion

Convert PDF documents to editable Word files:

```bash
POST /api/convert/pdf-to-word
```

**Parameters:**
- `file` - PDF file (multipart/form-data)

**Example:**

```bash
curl -X POST \
  -F "file=@document.pdf" \
  http://localhost:5001/api/convert/pdf-to-word \
  -o document.docx
```

### Word to PDF Conversion

Convert Word documents to PDF format:

```bash
POST /api/convert/word-to-pdf
```

**Parameters:**
- `file` - Word file (multipart/form-data)

**Example:**

```bash
curl -X POST \
  -F "file=@document.docx" \
  http://localhost:5001/api/convert/word-to-pdf \
  -o document.pdf
```

### Utility Endpoints

**Health Check:**
```bash
GET /api/health
```

**Supported Formats:**
```bash
GET /api/formats
```

**List Routes:**
```bash
GET /routes
```

## Configuration

Edit `.env` file:

```bash
HOST=localhost
PORT=5001
MAX_FILE_SIZE=10485760  # 10MB in bytes
```

## Project Structure

```
filea/
├── src/
│   ├── converters/         # Conversion logic
│   ├── route/             # API endpoints
│   ├── util/              # File handling utilities
│   └── server.py          # Main application
├── uploads/               # Temporary uploads
├── outputs/               # Converted files
└── requirements.txt       # Dependencies
```

## Development Roadmap

- [x] **Phase 1**: Image conversion (PNG, JPG, WEBP, AVIF, BMP, GIF)
- [x] **Phase 2**: PDF ↔ Word conversion
- [ ] **Phase 3**: Excel → PDF conversion
- [ ] **Phase 4**: File cleanup & optimization

## Libraries Used

- **Flask** - Web framework
- **Pillow** - Image processing
- **pillow-avif-plugin** - AVIF support
- **pdf2docx** - PDF to Word
- **python-docx** - Word documents
- **reportlab** - PDF generation
- **openpyxl** - Excel files

