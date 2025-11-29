# Server Start Guide

## ✅ Server is Running!

Your Flask File Conversion API is now running at:
**http://localhost:5001**

## Quick Test Commands

```bash
# Health Check
curl http://localhost:5001/api/health

# List Supported Formats
curl http://localhost:5001/api/formats

# Test Image Conversion (PNG to WEBP)
curl -X POST \
  -F "file=@image.png" \
  -F "to_format=webp" \
  http://localhost:5001/api/convert/image \
  -o output.webp

# Test PDF to Word
curl -X POST \
  -F "file=@document.pdf" \
  http://localhost:5001/api/convert/pdf-to-word \
  -o output.docx

# Test Word to PDF
curl -X POST \
  -F "file=@document.docx" \
  http://localhost:5001/api/convert/word-to-pdf \
  -o output.pdf

# Test PDF to Excel (NEW - Phase 3)
curl -X POST \
  -F "file=@data.pdf" \
  http://localhost:5001/api/convert/pdf-to-excel \
  -o output.xlsx

# Test Excel to PDF (NEW - Phase 3)
curl -X POST \
  -F "file=@spreadsheet.xlsx" \
  http://localhost:5001/api/convert/excel-to-pdf \
  -o output.pdf
```

## How to Start Server (Next Time)

```bash
cd /Users/pebi/Projects/Filea/filea-backend
cd src && HOST=localhost PORT=5001 python3 server.py
```

## Dependencies Installed

All required packages are now installed:
- ✅ Flask 0.10.1
- ✅ Flask-CORS 1.8.0
- ✅ Flask-RESTful 0.2.12
- ✅ Pillow 10.1.0 (image processing)
- ✅ PyMuPDF 1.23.26 (PDF handling)
- ✅ pdf2docx 0.5.8 (PDF to Word)
- ✅ python-docx 1.1.0 (Word documents)
- ✅ reportlab 4.0.7 (PDF generation)
- ✅ openpyxl 3.1.2 (Excel files)
- ✅ tabula-py 2.9.0 (PDF table extraction)
- ✅ pandas 2.1.3 (data manipulation)

## Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/formats` | GET | List supported formats |
| `/api/convert/image` | POST | Convert images |
| `/api/convert/pdf-to-word` | POST | PDF → Word |
| `/api/convert/word-to-pdf` | POST | Word → PDF |
| `/api/convert/pdf-to-excel` | POST | PDF → Excel ✨ NEW |
| `/api/convert/excel-to-pdf` | POST | Excel → PDF ✨ NEW |

## Next Steps

Ready to implement **Phase 4: PDF ↔ Image Conversion**?

This will add:
- PDF to Images (extract pages as PNG/JPG/WEBP)
- Images to PDF (single or multiple images)
