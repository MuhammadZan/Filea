# Phase 3 Testing Guide

## Excel Conversion Testing

### Prerequisites

1. Start the Flask server:
```bash
cd /Users/pebi/Projects/Filea/filea-backend
HOST=localhost PORT=5001 python3 src/server.py
```

2. Ensure you have test files ready:
   - A PDF file with tables (for PDF to Excel testing)
   - An Excel file (.xlsx or .xls) (for Excel to PDF testing)

---

## Test 1: PDF to Excel Conversion

### Test with cURL

```bash
# Convert PDF with tables to Excel
curl -X POST \
  -F "file=@test_data.pdf" \
  http://localhost:5001/api/convert/pdf-to-excel \
  -o output.xlsx
```

### Expected Results
- ✅ Returns `.xlsx` file
- ✅ Tables from PDF are extracted into separate sheets
- ✅ Each sheet is named `Table_1`, `Table_2`, etc.
- ✅ Headers are formatted (bold, centered)
- ✅ Column widths are auto-adjusted
- ✅ Original files are cleaned up after download

### Error Cases to Test

**No file provided:**
```bash
curl -X POST http://localhost:5001/api/convert/pdf-to-excel
# Expected: {"error": "No file provided"}
```

**Invalid file type:**
```bash
curl -X POST \
  -F "file=@image.png" \
  http://localhost:5001/api/convert/pdf-to-excel
# Expected: {"error": "Invalid file type. Expected: pdf"}
```

**PDF with no tables:**
```bash
curl -X POST \
  -F "file=@text_only.pdf" \
  http://localhost:5001/api/convert/pdf-to-excel
# Expected: {"error": "Conversion failed: No tables found in PDF..."}
```

---

## Test 2: Excel to PDF Conversion

### Test with cURL

```bash
# Convert Excel to PDF
curl -X POST \
  -F "file=@spreadsheet.xlsx" \
  http://localhost:5001/api/convert/excel-to-pdf \
  -o output.pdf
```

### Expected Results
- ✅ Returns `.pdf` file
- ✅ Each Excel sheet is rendered as a separate page (or section)
- ✅ Sheet names are included as headers (if multiple sheets)
- ✅ Tables are formatted with:
  - Blue header row with white text
  - Alternating row colors (white/light grey)
  - Grid lines and borders
- ✅ Data is properly aligned and readable
- ✅ Original files are cleaned up after download

### Error Cases to Test

**No file provided:**
```bash
curl -X POST http://localhost:5001/api/convert/excel-to-pdf
# Expected: {"error": "No file provided"}
```

**Invalid file type:**
```bash
curl -X POST \
  -F "file=@document.docx" \
  http://localhost:5001/api/convert/excel-to-pdf
# Expected: {"error": "Invalid file type. Expected: xlsx, xls"}
```

---

## Test 3: Supported Formats Endpoint

```bash
curl http://localhost:5001/api/formats
```

### Expected Response
```json
{
  "images": ["png", "jpg", "jpeg", "webp", "bmp", "gif", "avif"],
  "documents": ["pdf", "docx"],
  "spreadsheets": ["xlsx", "xls", "pdf"]
}
```

---

## Test 4: Health Check

```bash
curl http://localhost:5001/api/health
```

### Expected Response
```json
{
  "status": "healthy",
  "service": "File Conversion API",
  "version": "1.0.0"
}
```

---

## Integration Testing

### Test with Postman or Insomnia

1. **Import Collection:**
   - Create a new request collection
   - Add all endpoints

2. **PDF to Excel:**
   - Method: POST
   - URL: `http://localhost:5001/api/convert/pdf-to-excel`
   - Body: form-data
   - Key: `file`, Type: File, Value: [select PDF file]

3. **Excel to PDF:**
   - Method: POST
   - URL: `http://localhost:5001/api/convert/excel-to-pdf`
   - Body: form-data
   - Key: `file`, Type: File, Value: [select Excel file]

---

## Manual Verification Checklist

### PDF to Excel
- [ ] Open converted Excel file in Microsoft Excel or LibreOffice Calc
- [ ] Verify all tables are extracted
- [ ] Check data accuracy (compare with original PDF)
- [ ] Verify formatting (headers, column widths)
- [ ] Test with multi-page PDF
- [ ] Test with complex tables (merged cells, etc.)

### Excel to PDF
- [ ] Open converted PDF in a PDF reader
- [ ] Verify all sheets are included
- [ ] Check table formatting and readability
- [ ] Verify data integrity
- [ ] Test with multi-sheet Excel file
- [ ] Test with large datasets

---

## Performance Testing

### File Size Limits
- Test with files up to 10MB (configured limit)
- Test with files exceeding 10MB (should fail gracefully)

### Conversion Speed
- Small files (< 1MB): Should complete in < 5 seconds
- Medium files (1-5MB): Should complete in < 15 seconds
- Large files (5-10MB): Should complete in < 30 seconds

---

## Known Limitations

### PDF to Excel
- Only extracts tabular data (tables)
- Text-only PDFs will fail with "No tables found" error
- Complex table layouts may not convert perfectly
- Merged cells in PDF may not be preserved

### Excel to PDF
- Very wide tables may be truncated or scaled down
- Excel formulas are converted to their calculated values
- Charts and images are not included (only data)
- Cell formatting (colors, borders) from Excel is replaced with standard PDF table styling

---

## Troubleshooting

### Common Issues

**Issue: "No module named 'tabula'"**
```bash
python3 -m pip install tabula-py==2.9.0
```

**Issue: "No module named 'pandas'"**
```bash
python3 -m pip install pandas==2.1.3
```

**Issue: Java not found (for tabula-py)**
- tabula-py requires Java to be installed
- Install Java: `brew install openjdk` (macOS)
- Or download from: https://www.java.com/download/

**Issue: File cleanup not working**
- Check file permissions in `uploads/` and `outputs/` directories
- Ensure Flask has write permissions

---

## Next Steps

After successful testing:
1. ✅ Mark Phase 3 as complete in task.md
2. ✅ Update API Integration Guide with Excel endpoints
3. 🚀 Proceed to Phase 4: PDF ↔ Image conversion
