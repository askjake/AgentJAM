# Attachment File Type Expansion - Documentation

## Overview
Expanded Dish-Chat attachment support from 7 basic file types to **35+ MIME types** including:
- Email files (.eml, .msg)
- Office documents (.xlsx, .pptx, .csv)
- Code/markup files (.json, .xml, .yaml, .md, .html, .css, .js, .py, etc.)
- Archives with numbered extensions (.zip.001, .tar.gz.002, etc.)
- Log files with numbered extensions (.log.1, .log.2, etc.)

## Changes Summary

### 1. Config Changes (`app/config.py`)
**Added 4 New Configuration Lists:**

```python
SUPPORTED_LOG_TYPES: list[str] = [
    "text/plain",
    "application/gzip", 
    "application/x-gzip",
    "application/zip",
    "application/x-tar",
    "application/x-compressed-tar",
    "application/octet-stream",
]

SUPPORTED_EMAIL_TYPES: list[str] = [
    "message/rfc822",  # .eml files
    "application/vnd.ms-outlook",  # .msg files
    "application/octet-stream",
]

SUPPORTED_ADDITIONAL_DOC_TYPES: list[str] = [
    # Office formats
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # .xlsx
    "application/vnd.ms-excel",  # .xls
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",  # .pptx
    "application/vnd.ms-powerpoint",  # .ppt
    
    # Data formats
    "text/csv",
    "application/json",
    "application/xml",
    "text/xml",
    
    # Markup/code
    "text/markdown",
    "text/html",
    "text/css",
    "application/javascript",
    "text/javascript",
    "application/x-yaml",
    "text/yaml",
    "text/x-python",
    "text/x-java-source",
    "application/rtf",
]
```

### 2. Service Validation (`app/attachment/service.py`)
**Updated Upload Validation:**

```python
# OLD: Only checked DOC + IMAGE types
elif f.content_type in settings.SUPPORTED_DOC_TYPES + settings.SUPPORTED_IMAGE_TYPES:

# NEW: Checks all supported types
elif f.content_type in (
    settings.SUPPORTED_DOC_TYPES + 
    settings.SUPPORTED_IMAGE_TYPES + 
    settings.SUPPORTED_EMAIL_TYPES +
    settings.SUPPORTED_ADDITIONAL_DOC_TYPES
):
```

**Updated Preprocessing:**

```python
# Now embeds additional doc types and email files
embeddable_types = (
    settings.SUPPORTED_DOC_TYPES + 
    settings.SUPPORTED_ADDITIONAL_DOC_TYPES +
    settings.SUPPORTED_EMAIL_TYPES
)
if filetype in embeddable_types:
    await embed_document(...)
```

### 3. Storage Utils (`app/attachment/storage_utils.py`)
**Enhanced Numbered Extension Support:**

```python
def is_log_file(filename: str, content_type: str) -> bool:
    # Pattern 1: .log.1, .log.2, etc.
    if re.match(r'.*\.log\.\d+$', filename_lower):
        return True
    
    # Pattern 2: Numbered extensions like .001, .002, .003
    if re.match(r'.*\.\d{3,}$', filename_lower):
        return True
    
    # Pattern 3: Archive with numbered extension (.zip.001, .tar.gz.001)
    if re.match(r'.*\.(zip|tar|gz|tgz|rar|7z)\.\d+$', filename_lower):
        return True
```

## File Handling Strategy

### S3 + Embedded (Searchable)
- PDF documents
- Word documents (.docx)
- Excel spreadsheets (.xlsx)
- PowerPoint presentations (.pptx)
- Email files (.eml, .msg)
- Text/markup files (.txt, .md, .html, .json, .xml, .yaml)
- CSV files
- Code files (.py, .js, .java)

### Agent Sandbox Only (Not Embedded)
- Log files (.log, .log.1, .log.2)
- Archive files (.zip, .tar, .gz, .7z, .rar)
- Numbered split archives (.zip.001, .zip.002)
- Binary dumps

## Verification Results

✅ **Test Results:**
```
Total MIME types supported: 35
  - Document types: 3
  - Image types: 4
  - Log types: 7
  - Email types: 3
  - Additional doc types: 18

Numbered Extension Tests:
  ✅ server.log.1 → agent sandbox
  ✅ server.log.2 → agent sandbox
  ✅ archive.001 → agent sandbox
  ✅ archive.002 → agent sandbox
  ✅ backup.zip.001 → agent sandbox
  ✅ data.tar.gz.001 → agent sandbox
  ✅ email.eml → S3 + embedded
  ✅ document.pdf → S3 + embedded
  ✅ spreadsheet.xlsx → S3 + embedded
```

## Deployment Status

**Server:** agentpi003@10.73.184.61
**Service:** intelligent_backend.py (PID 15879)
**Status:** ✅ Running successfully
**Verification:** 51 conversations loaded, throttler state loaded

## Impact Assessment

### Risk Level: **LOW**
- Additive changes only (no existing functionality removed)
- All changes validated with syntax checks
- Service restarted successfully
- All original file types still supported

### Benefits:
- Users can now upload emails directly
- Excel/PowerPoint files can be analyzed
- Code files can be inspected
- Split archives handled properly
- Better numbered extension support

### No Changes Required For:
- Frontend (accepts any file, backend validates)
- Database schema
- Embedding pipeline (handles new types automatically)
- S3 storage configuration

## Testing Recommendations

1. **Upload various file types** through the UI
2. **Verify numbered extensions** (.log.1, .zip.001)
3. **Check email parsing** (.eml, .msg files)
4. **Test code file analysis** (.py, .js, .json)
5. **Validate Excel/CSV** data extraction

## Rollback Plan

If issues arise:
```bash
ssh agentpi003@10.73.184.61
cd /home/agentpi003/dish-chat/backend

# Restore from git (if tracked)
git checkout HEAD -- app/config.py app/attachment/service.py app/attachment/storage_utils.py

# Or restore from backups
cp app/config.py.backup app/config.py
cp app/attachment/service.py.backup app/attachment/service.py
cp app/attachment/storage_utils.py.backup app/attachment/storage_utils.py

# Restart service
pkill -f intelligent_backend.py
# (service auto-restarts via systemd/supervisor)
```

## Author
Jake (via Dish-Chat Agent)  
Date: 2026-04-15  
Server: agentpi003 (10.73.184.61)
