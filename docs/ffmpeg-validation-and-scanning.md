# FFmpeg Validation and MKV File Scanning

This document describes the FFmpeg validation and MKV file scanning features implemented in the batch converter.

## Table of Contents

1. [Overview](#overview)
2. [FFmpeg Validation](#ffmpeg-validation)
3. [MKV File Scanning](#mkv-file-scanning)
4. [Helper Scripts](#helper-scripts)
5. [API Reference](#api-reference)
6. [Examples](#examples)

---

## Overview

The batch converter includes two critical features:

- **FFmpeg Validation**: Ensures FFmpeg is properly installed and configured before processing
- **MKV File Scanning**: Discovers and catalogs MKV files in the input directory

These features are essential for reliable batch conversion and provide users with clear feedback about system requirements and available files.

---

## FFmpeg Validation

### Purpose

FFmpeg validation verifies that:
- FFmpeg is installed and accessible in the system PATH
- Required codecs are available (libx264, libx265, aac)
- Subtitle filter support is present
- FFprobe is available (optional but recommended)

### Implementation

The validation is implemented in `src/utils.py` with the following functions:

#### `validate_ffmpeg() -> bool`

Checks if FFmpeg is installed and accessible.

**Returns:**
- `True` if FFmpeg is working correctly
- `False` if FFmpeg is not found or not working

**Example:**
```python
from src.utils import validate_ffmpeg

if validate_ffmpeg():
    print("FFmpeg is ready!")
else:
    print("Please install FFmpeg")
```

#### `get_ffmpeg_version() -> Optional[str]`

Retrieves the FFmpeg version string.

**Returns:**
- Version string if available
- `None` if FFmpeg is not found

**Example:**
```python
from src.utils import get_ffmpeg_version

version = get_ffmpeg_version()
if version:
    print(f"FFmpeg version: {version}")
```

#### `validate_ffprobe() -> bool`

Checks if FFprobe is installed and accessible.

**Returns:**
- `True` if FFprobe is working
- `False` if FFprobe is not found

---

## MKV File Scanning

### Purpose

MKV file scanning:
- Recursively searches the input directory for `.mkv` files
- Filters out hidden files and system files
- Sorts files alphabetically for consistent processing
- Provides file metadata (size, path, conversion status)

### Implementation

The scanning is implemented in the `BatchConverter` class in `src/converter.py`.

#### `scan_input_folder() -> list[Path]`

Scans the input folder for MKV files.

**Returns:**
- Sorted list of `Path` objects pointing to MKV files

**Features:**
- Recursive directory traversal
- Hidden file filtering (files/folders starting with `.`)
- Alphabetical sorting
- Error handling for missing or invalid input directories

**Example:**
```python
from src.config import load_config
from src.converter import BatchConverter

config = load_config()
converter = BatchConverter(config)

mkv_files = converter.scan_input_folder()
print(f"Found {len(mkv_files)} MKV files")
```

### Filtering Rules

The scanner applies these filtering rules:

1. **File Extension**: Only files ending in `.mkv` (case-sensitive)
2. **Hidden Files**: Excludes files or directories starting with `.`
3. **Recursive Search**: Searches all subdirectories
4. **Sorting**: Alphabetical by full path

**Example Directory Structure:**
```
input/
├── movie1.mkv              ✅ Included
├── movie2.mkv              ✅ Included
├── .hidden.mkv             ❌ Excluded (hidden)
├── subfolder/
│   ├── episode1.mkv        ✅ Included
│   └── episode2.mkv        ✅ Included
└── .backup/
    └── old.mkv             ❌ Excluded (hidden directory)
```

---

## Helper Scripts

Two helper scripts are provided for easy testing and validation:

### 1. FFmpeg Validation Script

**Location:** `scripts/validate_ffmpeg.py`

**Purpose:** Comprehensive FFmpeg installation checker

**Usage:**
```bash
# Using virtual environment
.venv/bin/python scripts/validate_ffmpeg.py

# Or directly
python scripts/validate_ffmpeg.py
```

**Features:**
- FFmpeg installation check
- Version detection
- Codec availability verification (libx264, libx265, aac)
- Subtitle filter support check
- FFprobe availability check
- Detailed error messages with installation instructions

**Output Example:**
```
============================================================
           FFmpeg Installation Validator
============================================================

🔍 Checking FFmpeg installation...
✅ FFmpeg is installed
   Version: ffmpeg version 6.0 Copyright (c) 2000-2023 the FFmpeg developers

🔍 Checking FFprobe installation...
✅ FFprobe is installed

🔍 Checking required codecs...
✅ libx264: Available
✅ libx265: Available
✅ aac: Available

🔍 Checking subtitle filter support...
✅ Subtitle filter is available

============================================================
✅ All checks passed! FFmpeg is properly configured.
============================================================
```

### 2. MKV File Scanner Script

**Location:** `scripts/scan_mkv_files.py`

**Purpose:** Scan and display MKV files with detailed information

**Usage:**
```bash
# Basic usage
.venv/bin/python scripts/scan_mkv_files.py

# With custom config
python scripts/scan_mkv_files.py --config custom_config.yaml

# Show detailed video information (requires ffprobe)
python scripts/scan_mkv_files.py --details
```

**Features:**
- File discovery and counting
- File size calculation
- Conversion status (already converted vs pending)
- Optional detailed video information (codec, resolution, duration)
- Summary statistics

**Output Example:**
```
============================================================
              MKV File Scanner
============================================================

📁 Scanning directory: input
📁 Output directory: output
🎬 Target resolution: 480p

🔍 Scanning for MKV files...

📊 Summary:
   Total MKV files found: 5
   Already converted: 2
   Pending conversion: 3
   Total size: 12.5 GB

📋 File List:
============================================================

  📄 movie1.mkv
     Path: input/movie1.mkv
     Size: 2.5 GB
     Status: ✅ Converted

  📄 movie2.mkv
     Path: input/movie2.mkv
     Size: 3.2 GB
     Status: ⏳ Pending

  📄 series/episode1.mkv
     Path: input/series/episode1.mkv
     Size: 1.8 GB
     Status: ⏳ Pending

============================================================
✨ 3 file(s) ready for conversion
   Run 'python main.py' to start converting
============================================================
```

**Command Line Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--config PATH` | Path to configuration file | config.yaml |
| `--details` | Show detailed video information | False |

---

## API Reference

### Core Functions

#### `validate_ffmpeg() -> bool`
**Module:** `src.utils`

Validates FFmpeg installation.

**Returns:**
- `bool`: Installation status

**Raises:**
- None (catches all exceptions internally)

---

#### `get_ffmpeg_version() -> Optional[str]`
**Module:** `src.utils`

Gets FFmpeg version string.

**Returns:**
- `Optional[str]`: Version string or None

---

#### `validate_ffprobe() -> bool`
**Module:** `src.utils`

Validates FFprobe installation.

**Returns:**
- `bool`: Installation status

---

#### `scan_input_folder() -> list[Path]`
**Module:** `src.converter.BatchConverter`

Scans input directory for MKV files.

**Returns:**
- `list[Path]`: List of MKV file paths

**Side Effects:**
- Logs information about found files
- Logs errors if directory is missing/invalid

---

### Helper Functions

#### `get_video_info(video_path: Path) -> dict[str, str]`
**Module:** `src.utils`

Extracts video metadata using FFprobe.

**Parameters:**
- `video_path`: Path to video file

**Returns:**
- `dict[str, str]`: Video metadata (codec, resolution, duration)

**Example:**
```python
from pathlib import Path
from src.utils import get_video_info

info = get_video_info(Path("input/movie.mkv"))
print(f"Resolution: {info['width']}x{info['height']}")
print(f"Codec: {info['codec_name']}")
```

---

## Examples

### Example 1: Pre-flight Check

```python
"""Check system requirements before conversion."""

from src.utils import validate_ffmpeg, validate_ffprobe
from loguru import logger

def preflight_check() -> bool:
    """Run pre-flight checks before conversion."""

    # Check FFmpeg
    if not validate_ffmpeg():
        logger.error("FFmpeg not found. Please install FFmpeg.")
        return False

    # Check FFprobe (optional)
    if not validate_ffprobe():
        logger.warning("FFprobe not found. Some features may be limited.")

    logger.info("All checks passed!")
    return True

if __name__ == "__main__":
    if preflight_check():
        print("Ready to convert!")
    else:
        print("Please fix the issues above.")
```

### Example 2: Scan and Report

```python
"""Scan input folder and generate report."""

from src.config import load_config
from src.converter import BatchConverter

def generate_scan_report() -> None:
    """Generate a report of files ready for conversion."""

    config = load_config()
    converter = BatchConverter(config)

    mkv_files = converter.scan_input_folder()

    if not mkv_files:
        print("No MKV files found.")
        return

    total_size = sum(f.stat().st_size for f in mkv_files)
    total_size_gb = total_size / (1024**3)

    print(f"\nScan Report")
    print(f"=" * 50)
    print(f"Files found: {len(mkv_files)}")
    print(f"Total size: {total_size_gb:.2f} GB")
    print(f"\nFiles:")
    for i, mkv_file in enumerate(mkv_files, 1):
        size_mb = mkv_file.stat().st_size / (1024**2)
        print(f"  {i}. {mkv_file.name} ({size_mb:.1f} MB)")

if __name__ == "__main__":
    generate_scan_report()
```

### Example 3: Conditional Processing

```python
"""Process files only if FFmpeg is available."""

from src.config import load_config
from src.converter import BatchConverter
from src.utils import validate_ffmpeg
from loguru import logger

def smart_convert() -> None:
    """Convert files with automatic FFmpeg validation."""

    # Validate FFmpeg first
    if not validate_ffmpeg():
        logger.error("Cannot proceed without FFmpeg. Please install it first.")
        logger.info("macOS: brew install ffmpeg")
        logger.info("Ubuntu: sudo apt install ffmpeg")
        return

    # Load config and create converter
    config = load_config()
    converter = BatchConverter(config)

    # Scan for files
    mkv_files = converter.scan_input_folder()

    if not mkv_files:
        logger.info("No MKV files to process.")
        return

    logger.info(f"Found {len(mkv_files)} file(s) to convert")

    # Process all files
    results = converter.process_all(mkv_files)

    # Generate summary
    converter.generate_summary(results)

if __name__ == "__main__":
    smart_convert()
```

---

## Troubleshooting

### FFmpeg Not Found

**Problem:** `validate_ffmpeg()` returns `False`

**Solutions:**
1. Install FFmpeg:
   ```bash
   # macOS
   brew install ffmpeg

   # Ubuntu/Debian
   sudo apt install ffmpeg

   # Windows
   choco install ffmpeg
   ```

2. Verify installation:
   ```bash
   ffmpeg -version
   ```

3. Check PATH:
   ```bash
   which ffmpeg  # macOS/Linux
   where ffmpeg  # Windows
   ```

### No Files Found

**Problem:** `scan_input_folder()` returns empty list

**Solutions:**
1. Check input folder exists:
   ```bash
   ls -la input/
   ```

2. Verify file extension is `.mkv` (case-sensitive)

3. Check for hidden directories:
   ```bash
   find input/ -name "*.mkv"
   ```

4. Verify config.yaml has correct input_folder path

### Permission Denied

**Problem:** Cannot read input directory

**Solutions:**
1. Check directory permissions:
   ```bash
   chmod 755 input/
   ```

2. Verify file permissions:
   ```bash
   chmod 644 input/*.mkv
   ```

---

## Performance Considerations

### FFmpeg Validation

- **Cost:** ~10-50ms per validation
- **Caching:** Results are not cached; validate once at startup
- **Recommendation:** Call `validate_ffmpeg()` once before batch processing

### MKV Scanning

- **Cost:** ~1-5ms per file for basic scan
- **Cost with details:** ~50-200ms per file (requires FFprobe)
- **Recommendation:** Use `--details` flag only when needed

**Optimization Example:**
```python
# Good: Validate once
if validate_ffmpeg():
    converter = BatchConverter(config)
    mkv_files = converter.scan_input_folder()
    results = converter.process_all(mkv_files)

# Bad: Validate per file
for mkv_file in mkv_files:
    if validate_ffmpeg():  # Don't do this!
        convert(mkv_file)
```

---

## Integration with Main Converter

The validation and scanning features are integrated into the main conversion workflow:

```python
# From main.py
from src.config import load_config
from src.converter import BatchConverter
from src.utils import validate_ffmpeg
from loguru import logger

def main() -> None:
    """Main entry point."""

    # Step 1: Validate FFmpeg (Step 2 from project plan)
    if not validate_ffmpeg():
        logger.error("FFmpeg not found in PATH")
        return

    # Step 2: Load config
    config = load_config()

    # Step 3: Scan for files (Step 3 from project plan)
    converter = BatchConverter(config)
    mkv_files = converter.scan_input_folder()

    if not mkv_files:
        logger.info("No MKV files found")
        return

    # Step 4: Process files
    results = converter.process_all(mkv_files)
    converter.generate_summary(results)
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-06 | Initial implementation of FFmpeg validation and MKV scanning |

---

## Related Documentation

- [Project Plan](../docs/plans/project-plan.md) - Overall project architecture
- [README.md](../README.md) - User guide and quick start
- [Configuration Guide](../README.md#configuration-guide) - YAML configuration details

---

**Last Updated:** December 6, 2025
**Author:** Project Team
**Status:** ✅ Implemented and Tested
