# Debug Directory

This directory contains debugging and testing scripts for development purposes.

## Contents

### test_thai_fonts.py

Test script for verifying Thai font rendering with tone marks and diacritics.

**Purpose:**
- Tests Thai character rendering including tone marks (้ ่ ๊ ๋)
- Verifies proper display of Thai vowels (ั ิ ี ึ ื ุ ู)
- Checks FFmpeg subtitle filter configuration
- Lists available Thai fonts on the system

**Usage:**
```bash
python debug/test_thai_fonts.py
# or
./debug/test_thai_fonts.py
```

**What it does:**
1. Displays system information
2. Checks FFmpeg installation
3. Lists available Thai fonts
4. Shows Thai text test samples
5. Creates a test SRT subtitle file
6. Provides manual testing instructions

**Test Samples:**
The script includes various Thai text samples covering:
- Common phrases with tone marks
- Tone mark variations (่ ้ ๊ ๋)
- Vowel combinations (สระ)
- Complex words with multiple diacritics

## Notes

- This directory is excluded from version control (see .gitignore)
- Generated test files (*.srt, *.mp4, etc.) are temporary
- Use these scripts for debugging subtitle rendering issues
