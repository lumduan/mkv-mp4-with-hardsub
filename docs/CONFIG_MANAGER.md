# 🛠️ Configuration Manager Guide

The Configuration Manager is an interactive CLI tool that provides a user-friendly interface for managing the `config.yaml` settings file. It's designed to make configuration management simple and accessible for both first-time users and advanced users.

## 📋 Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Quick Setup Wizard](#quick-setup-wizard)
- [Advanced Configuration Menu](#advanced-configuration-menu)
- [Configuration Options](#configuration-options)
- [Use Cases & Examples](#use-cases--examples)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Overview

### What is the Configuration Manager?

The Configuration Manager (`scripts/config_manager.py`) is an interactive menu-driven tool that allows you to:

- **Quick Setup**: Run a guided wizard for first-time configuration
- **View Settings**: Display current configuration in organized sections
- **Update Settings**: Modify settings by category with validation
- **Get Help**: Access built-in documentation and tips
- **Save/Load**: Persist changes to disk or reload from file
- **Reset**: Restore factory default settings

### Why Use the Configuration Manager?

- **No YAML Knowledge Required**: Interactive menus instead of manual editing
- **Real-time Validation**: Catches errors before saving
- **Built-in Help**: Comprehensive documentation at your fingertips
- **Smart Defaults**: Optimal settings for common use cases
- **Safe Configuration**: Preview changes before applying

## Getting Started

### Prerequisites

1. Python 3.10 or higher installed
2. Project dependencies installed (`uv sync`)
3. FFmpeg installed and in PATH

### Launching the Configuration Manager

From the project root directory:

```bash
# Using the virtual environment directly (recommended)
.venv/bin/python scripts/config_manager.py

# Or activate the virtual environment first
source .venv/bin/activate
python scripts/config_manager.py

# With a custom config file
.venv/bin/python scripts/config_manager.py path/to/custom_config.yaml
```

### First Run Experience

On first run (when `config.yaml` doesn't exist), you'll see:

```text
======================================================================
               🎬 MKV to MP4 Converter
               Configuration Manager
======================================================================

📝 About config.yaml:
   The config.yaml file controls how your videos are converted.
   You can customize:
   • Video quality (resolution, codec, quality level)
   • Audio settings (codec, bitrate)
   • Subtitle preferences (language, styling)
   • Processing options (parallel processing, etc.)

💡 Tips:
   • Lower CRF value = Better quality but larger file size
   • Higher resolution = Better quality but slower conversion
   • Enable parallel processing if you have a multi-core CPU
======================================================================

🎯 It looks like this is your first time setting up.
Would you like to run the Quick Setup Wizard? (yes/no) [yes]:
```

## Quick Setup Wizard

The Quick Setup Wizard is designed for first-time users or when you want to quickly reconfigure the converter with sensible defaults.

### What the Wizard Configures

1. **Quality Preset**: Choose from 3 optimized presets
2. **Subtitle Settings**: Enable/disable subtitle burning and select language
3. **Performance Options**: Configure parallel processing
4. **Directory Paths**: Set input/output folder locations

### Step-by-Step Walkthrough

#### Step 1: Choose Quality Preset

```text
📊 Choose quality preset:
  1. High Quality (720p, CRF 20) - Larger files, better quality
  2. Balanced (480p, CRF 24) - Recommended for most users
  3. Smaller Files (480p, CRF 28) - Faster conversion, smaller files

Select preset (1-3) [2]: 2
✓ Balanced preset selected
```

**What This Sets:**
- **Option 1**: Resolution=720p, CRF=20, Best for archiving or high-quality viewing
- **Option 2**: Resolution=480p, CRF=24, Good balance of quality and file size
- **Option 3**: Resolution=480p, CRF=28, Smallest files, faster encoding

#### Step 2: Configure Subtitles

```text
📝 Subtitle settings:
Do you want to burn subtitles into the video? (yes/no) [yes]: yes
Preferred subtitle language code (e.g., eng, tha, jpn) [auto]: eng
✓ Will use 'eng' subtitles when available
```

**Language Codes:**
- `eng` - English
- `tha` - Thai
- `jpn` - Japanese
- `chi` - Chinese
- `spa` - Spanish
- `fra` - French
- Leave blank or type `auto` for default subtitle track

#### Step 3: Performance Settings

```text
⚙️  Performance settings:
Enable parallel processing for faster conversion? (yes/no) [no]: yes
How many files to process simultaneously? (1-4) [2]: 2
✓ Will process 2 files in parallel
```

**⚠️ Important Notes:**
- Parallel processing uses more CPU and RAM
- Recommended workers = CPU cores - 1
- Start with 2 workers and adjust based on system performance

#### Step 4: Directory Configuration

```text
📁 Directory settings:
   Input folder:  Where your MKV files are located
   Output folder: Where converted MP4 files will be saved

Use default folders (input/, output/)? (yes/no) [yes]: yes
```

**Default Directories:**
- `input/` - Place your MKV files here
- `output/` - Converted MP4 files go here
- `logs/` - Processing logs

#### Step 5: Review and Save

```text
✨ Setup complete! Your configuration:
======================================================================
CURRENT CONFIGURATION
======================================================================

📁 Directory Settings:
   Input Folder:    input
   Output Folder:   output
   Logs Folder:     logs

🎬 Video Settings:
   Resolution:      480p
   Codec:           libx264
   CRF (Quality):   24
   Preset:          medium

🔊 Audio Settings:
   Codec:           aac
   Bitrate:         128k

📝 Subtitle Settings:
   Enabled:         True
   Language:        eng
   Force Style:     None

⚙️  Processing Options:
   Parallel:        False
   Max Workers:     2
   Skip Existing:   True
   Verbose:         False
======================================================================

💾 Save this configuration to config.yaml? (yes/no) [yes]: yes
✓ Configuration saved to config.yaml

✅ Configuration saved! You can now run the converter.
   To make changes later, run this script again.
```

## Advanced Configuration Menu

For detailed control over all settings, use the main menu.

### Main Menu Options

```text
📋 Main Menu:
  1. View current configuration
  2. 🚀 Quick Setup Wizard (Easy configuration)
  3. Update directory settings
  4. Update video settings
  5. Update audio settings
  6. Update subtitle settings
  7. Update processing options
  8. Save configuration
  9. Reset to defaults
  R. Reload configuration from file
  H. Show help and tips
  0. Exit
```

### Option 1: View Current Configuration

Displays all current settings organized by category:
- Directory settings
- Video encoding settings
- Audio encoding settings
- Subtitle settings
- Processing options

### Option 3: Update Directory Settings

```text
📁 Directory Settings
----------------------------------------
Input folder [input]: /path/to/my/videos
Output folder [output]: /path/to/converted
Logs folder [logs]: /path/to/logs
✓ Directory settings updated
```

**Tips:**
- Use absolute paths for clarity
- Ensure directories exist or will be created automatically
- Relative paths are resolved from project root

### Option 4: Update Video Settings

```text
🎬 Video Encoding Settings
----------------------------------------
Resolution (144-2160) [480]: 720

Available codecs: libx264, libx265, h264, hevc
Video codec [libx264]: libx264

CRF quality (0-51, lower=better) [24]: 23

Available presets: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
Encoding preset [medium]: slow
✓ Video settings updated
```

#### Resolution Guidelines

| Resolution | Quality | Use Case | File Size |
|------------|---------|----------|-----------|
| 480p | SD | Mobile, small screens | Small |
| 720p | HD | Laptops, tablets | Medium |
| 1080p | Full HD | Large screens, archival | Large |

#### CRF (Constant Rate Factor) Guidelines

| CRF Range | Quality | Description | File Size |
|-----------|---------|-------------|-----------|
| 18-20 | Excellent | Near-lossless, archival | Very Large |
| 21-23 | Very Good | High quality, minimal artifacts | Large |
| 24-26 | Good | Balanced quality/size (recommended) | Medium |
| 27-30 | Fair | Noticeable compression, smaller files | Small |
| 31+ | Poor | Heavy compression, visible artifacts | Very Small |

#### Codec Comparison

| Codec | Compatibility | Compression | Speed | Best For |
|-------|---------------|-------------|-------|----------|
| libx264 | Excellent | Good | Fast | General use, compatibility |
| libx265 | Good | Excellent | Slow | Smaller files, modern devices |

#### Encoding Presets

| Preset | Speed | Compression | CPU Usage | Use Case |
|--------|-------|-------------|-----------|----------|
| ultrafast | Fastest | Poor | Low | Quick tests |
| fast | Very Fast | Fair | Medium | Fast turnaround |
| medium | Balanced | Good | Medium | Default (recommended) |
| slow | Slow | Very Good | High | Quality priority |
| veryslow | Very Slow | Best | Very High | Maximum compression |

### Option 5: Update Audio Settings

```text
🔊 Audio Encoding Settings
----------------------------------------
Available codecs: aac, mp3, opus, ac3
Audio codec [aac]: aac

Audio bitrate (e.g., 128k, 192k) [128k]: 192k
✓ Audio settings updated
```

#### Audio Codec Guidelines

| Codec | Quality | Compatibility | Bitrate Range | Best For |
|-------|---------|---------------|---------------|----------|
| AAC | Excellent | Excellent | 96k-256k | Default choice |
| MP3 | Good | Universal | 128k-320k | Maximum compatibility |
| Opus | Excellent | Good | 64k-192k | Modern devices, best quality/size |
| AC3 | Good | Good | 128k-640k | Home theater systems |

#### Bitrate Guidelines

| Bitrate | Quality | File Size | Use Case |
|---------|---------|-----------|----------|
| 96k | Fair | Smallest | Voice, podcasts |
| 128k | Good | Small | Standard quality (recommended) |
| 192k | Very Good | Medium | Music, high-quality audio |
| 256k+ | Excellent | Large | Audiophile, archival |

### Option 6: Update Subtitle Settings

```text
📝 Subtitle Settings
----------------------------------------
Enable subtitles? (yes/no) [yes]: yes

Subtitle language code (or blank for default) [eng]: tha

Custom subtitle style (or blank) []: FontName=Arial,FontSize=24,PrimaryColour=&H00FFFFFF
✓ Subtitle settings updated
```

#### Subtitle Language Codes

Common ISO 639-2/3 language codes:
- `eng` - English
- `tha` - Thai
- `jpn` - Japanese
- `chi` - Chinese (Simplified)
- `zho` - Chinese (Traditional)
- `kor` - Korean
- `spa` - Spanish
- `fra` - French
- `ger` - German
- `rus` - Russian
- `ara` - Arabic
- `por` - Portuguese

#### Custom Subtitle Styling

The `force_style` option allows you to override subtitle appearance. Example styles:

```text
# White text, Arial font, size 24
FontName=Arial,FontSize=24,PrimaryColour=&H00FFFFFF

# Yellow text with black outline
FontName=Arial,FontSize=20,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,Outline=2

# Bold text with shadow
FontName=Arial,FontSize=22,Bold=1,Shadow=2
```

**Style Parameters:**
- `FontName` - Font family (Arial, Times New Roman, etc.)
- `FontSize` - Size in points (16-32 typical)
- `PrimaryColour` - Text color in &HAABBGGRR format
- `OutlineColour` - Outline color
- `Outline` - Outline width (0-4)
- `Shadow` - Shadow depth (0-4)
- `Bold` - Bold text (0 or 1)
- `Italic` - Italic text (0 or 1)

### Option 7: Update Processing Options

```text
⚙️  Processing Options
----------------------------------------
Enable parallel processing? (yes/no) [no]: yes

Max workers (1-16) [2]: 4

Skip existing files? (yes/no) [yes]: yes

Enable verbose logging? (yes/no) [no]: no
✓ Processing options updated
```

#### Parallel Processing Guidelines

**When to Enable:**
- You have multiple MKV files to convert
- Your CPU has 4+ cores
- You have sufficient RAM (8GB+ recommended)

**When to Disable:**
- Single file conversion
- Limited CPU resources
- Stability issues

**Worker Count Recommendations:**
| CPU Cores | Recommended Workers | Notes |
|-----------|-------------------|-------|
| 2 | 1 | No parallel benefit |
| 4 | 2-3 | Good balance |
| 6 | 3-4 | Efficient use |
| 8+ | 4-6 | Maximum performance |

**Formula**: `workers = (CPU_cores - 1)` or `CPU_cores / 2`

### Option H: Help System

Press `H` to access comprehensive help documentation covering:
- Video settings explained (resolution, CRF, codec, preset)
- Audio codec recommendations with use cases
- Subtitle configuration details
- Processing option guidelines
- Common quality presets for different scenarios
- File location information
- Tips and best practices

### Option 8: Save Configuration

Saves current settings to `config.yaml` (or custom path).

```text
✓ Configuration saved to config.yaml
```

### Option 9: Reset to Defaults

Restores factory default settings with confirmation:

```text
⚠️  Are you sure you want to reset to default configuration? (yes/no): yes
✓ Configuration reset to defaults
```

**Default Settings:**
- Resolution: 480p
- Video Codec: libx264
- CRF: 24
- Preset: medium
- Audio Codec: AAC
- Audio Bitrate: 128k
- Subtitles: Enabled
- Parallel Processing: Disabled
- Skip Existing: Enabled

### Option R: Reload Configuration

Reloads settings from disk, discarding unsaved changes:

```text
✓ Configuration loaded from config.yaml
```

Useful when:
- You've made changes but want to undo them
- Another process has modified the config file
- You want to verify saved settings

## Configuration Options

### Complete Settings Reference

#### Directory Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `input_folder` | Path | `input` | Source directory for MKV files |
| `output_folder` | Path | `output` | Destination for converted MP4 files |
| `logs_folder` | Path | `logs` | Directory for log files |

#### Video Encoding Settings

| Setting | Type | Range | Default | Description |
|---------|------|-------|---------|-------------|
| `resolution` | int | 144-2160 | 480 | Target video height in pixels |
| `codec` | str | See codecs | libx264 | Video encoder |
| `crf` | int | 0-51 | 24 | Quality level (lower = better) |
| `preset` | str | See presets | medium | Encoding speed vs compression |

**Valid Codecs:**
- `libx264` - H.264/AVC (recommended)
- `libx265` - H.265/HEVC
- `h264` - H.264 (hardware)
- `hevc` - HEVC (hardware)

**Valid Presets:**
- `ultrafast`, `superfast`, `veryfast`
- `faster`, `fast`, `medium`
- `slow`, `slower`, `veryslow`

#### Audio Encoding Settings

| Setting | Type | Options | Default | Description |
|---------|------|---------|---------|-------------|
| `codec` | str | See codecs | aac | Audio encoder |
| `bitrate` | str | e.g., 128k | 128k | Audio quality |

**Valid Codecs:**
- `aac` - Advanced Audio Coding (recommended)
- `mp3` - MPEG-1 Audio Layer 3
- `opus` - Opus codec
- `ac3` - Dolby Digital

#### Subtitle Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `enabled` | bool | true | Enable subtitle burning |
| `language` | str/null | null | Preferred subtitle language (ISO 639 code) |
| `force_style` | str/null | null | Custom ASS subtitle styling |

#### Processing Options

| Setting | Type | Range | Default | Description |
|---------|------|-------|---------|-------------|
| `parallel_processing` | bool | - | false | Enable multi-file processing |
| `max_workers` | int | 1-16 | 2 | Number of concurrent conversions |
| `skip_existing` | bool | - | true | Skip files already converted |
| `verbose` | bool | - | false | Enable debug logging |

## Use Cases & Examples

### Use Case 1: Quick Setup for New Users

**Scenario**: First-time user wants to convert videos with reasonable defaults.

**Steps:**
1. Launch config manager: `.venv/bin/python scripts/config_manager.py`
2. Select "yes" for Quick Setup Wizard
3. Choose preset 2 (Balanced)
4. Enable subtitles with "eng" language
5. Disable parallel processing (for safety)
6. Use default directories
7. Save configuration

**Result**: Ready-to-use configuration optimized for quality and compatibility.

### Use Case 2: High-Quality Archival

**Scenario**: Convert important videos for long-term storage.

**Configuration:**
- Resolution: 1080p
- CRF: 18
- Preset: slower
- Audio: AAC 192k
- Subtitles: Enabled, force English

**Steps:**
1. Launch config manager
2. Select option 4 (Update video settings)
   - Resolution: 1080
   - CRF: 18
   - Preset: slower
3. Select option 5 (Update audio settings)
   - Bitrate: 192k
4. Select option 8 (Save configuration)

**Result**: Maximum quality output with larger file sizes.

### Use Case 3: Batch Processing for Mobile

**Scenario**: Convert many files for viewing on mobile devices.

**Configuration:**
- Resolution: 480p
- CRF: 28
- Preset: fast
- Parallel: Yes, 4 workers
- Skip existing: Yes

**Steps:**
1. Launch config manager
2. Run Quick Setup Wizard
   - Select preset 3 (Smaller Files)
   - Enable subtitles as needed
   - Enable parallel processing with 4 workers
3. Save configuration
4. Place all MKV files in input folder
5. Run main converter

**Result**: Fast batch conversion with small file sizes.

### Use Case 4: Subtitle Language Override

**Scenario**: Force specific subtitle track for multi-language videos.

**Steps:**
1. Launch config manager
2. Select option 6 (Update subtitle settings)
3. Enable subtitles: yes
4. Language code: tha (for Thai)
5. Save configuration

**Result**: All conversions will prioritize Thai subtitles.

### Use Case 5: Testing Different Quality Settings

**Scenario**: Find optimal quality/size balance for your content.

**Method 1 - Using Config Manager:**
1. Convert one file with CRF 24
2. Reload config manager
3. Change CRF to 26
4. Convert same file to different output
5. Compare file sizes and quality

**Method 2 - Multiple Config Files:**
```bash
# Create test configs
cp config.yaml config.crf24.yaml
cp config.yaml config.crf26.yaml

# Edit each manually or use config manager
.venv/bin/python scripts/config_manager.py config.crf24.yaml
# Set CRF to 24, save, exit

.venv/bin/python scripts/config_manager.py config.crf26.yaml
# Set CRF to 26, save, exit

# Test conversions (future feature)
python main.py --config config.crf24.yaml
python main.py --config config.crf26.yaml
```

## Troubleshooting

### Python Version Warnings

**Issue:**
```text
⚠️  WARNING: You are using Python 3.14 alpha version!
   This may cause crashes with some dependencies (pydantic).
```

**Solution:**
- Use Python 3.10, 3.11, 3.12, or 3.13 stable release
- Check version: `python --version`
- Install stable Python via pyenv, conda, or system package manager

### Module Import Errors

**Issue:**
```text
❌ Error loading configuration modules: No module named 'pydantic'
```

**Solutions:**
1. Install dependencies: `uv sync`
2. Verify virtual environment: `which python` (should show `.venv/bin/python`)
3. Check Python version compatibility
4. Reinstall pydantic: `uv pip install pydantic`

### Configuration Validation Errors

**Issue:**
```text
✗ Invalid codec 'libx265'. Must be one of: libx264, h264, hevc
```

**Solution:**
- Check allowed values in error message
- Refer to configuration options tables above
- Use help system (press H) for guidance

### File Permission Issues

**Issue:**
```text
✗ Error saving configuration: Permission denied
```

**Solutions:**
1. Check file permissions: `ls -l config.yaml`
2. Ensure you have write access: `chmod 644 config.yaml`
3. Run from correct directory (project root)
4. Check directory permissions: `ls -ld .`

### Config Not Loading

**Issue:**
```text
✗ Error loading configuration: Invalid YAML syntax
```

**Solutions:**
1. Validate YAML: `python -c "import yaml; yaml.safe_load(open('config.yaml'))"`
2. Reset to defaults (option 9 in menu)
3. Check for tabs (YAML uses spaces only)
4. Verify indentation (2 or 4 spaces consistently)

### Parallel Processing Issues

**Issue:** System becomes unresponsive or conversions fail when parallel processing enabled.

**Solutions:**
1. Reduce max_workers to 2
2. Disable parallel processing
3. Check system resources: `htop` or Activity Monitor
4. Ensure sufficient RAM (8GB+ recommended)
5. Close other applications during conversion

## Best Practices

### 1. Start with Defaults

Use the Quick Setup Wizard or default settings for your first conversion:
- Test with one file first
- Verify output quality and file size
- Adjust settings based on results

### 2. Test Before Batch Processing

Before converting a large batch:
1. Convert one sample file
2. Check video quality on your target device
3. Verify subtitle readability
4. Confirm file size is acceptable
5. Then process remaining files

### 3. Use Appropriate Quality Settings

**For archival/important content:**
- Resolution: Original or 1080p
- CRF: 18-20
- Preset: slow/slower

**For general viewing:**
- Resolution: 480p-720p
- CRF: 23-24
- Preset: medium

**For storage-constrained scenarios:**
- Resolution: 480p
- CRF: 26-28
- Preset: fast/medium

### 4. Enable Skip Existing

Always keep `skip_existing: true` to:
- Avoid re-converting files
- Save time on reruns
- Prevent accidental overwrites

### 5. Monitor First Parallel Run

When enabling parallel processing:
1. Start with 2 workers
2. Monitor CPU and RAM usage
3. Watch for errors or crashes
4. Gradually increase workers if stable

### 6. Save Configurations

Create multiple config files for different scenarios:
```bash
config.yaml           # Default balanced settings
config.hq.yaml       # High quality archival
config.mobile.yaml   # Small files for mobile
config.fast.yaml     # Quick conversions
```

### 7. Regular Backups

Before making major changes:
```bash
cp config.yaml config.backup.yaml
```

### 8. Use Version Control

Track configuration changes with git:
```bash
git add config.yaml
git commit -m "Update video quality to 720p"
```

### 9. Document Custom Settings

Add comments to manual YAML edits:
```yaml
video:
  resolution: 720  # Using 720p for HD quality on tablets
  crf: 22          # Slightly better than default for archival
```

### 10. Leverage Help System

- Press `H` anytime for comprehensive help
- Reference built-in documentation
- Check examples for common presets
- Review quality guidelines before changing settings

## Environment Variables

The config manager and converter support environment variable overrides:

```bash
# Override video resolution
export CONVERTER_VIDEO__RESOLUTION=720

# Override subtitle language
export CONVERTER_SUBTITLES__LANGUAGE=tha

# Enable verbose mode
export CONVERTER_VERBOSE=true

# Launch config manager (settings will reflect overrides)
.venv/bin/python scripts/config_manager.py
```

**Note:** Environment variables take precedence over `config.yaml` values.

## Advanced Tips

### Custom Subtitle Styles

Create visually appealing subtitles with custom styling:

```yaml
subtitles:
  enabled: true
  language: eng
  force_style: "FontName=Arial,FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Shadow=1"
```

**Color Format:** `&HAABBGGRR` (Alpha, Blue, Green, Red in hex)
- White: `&H00FFFFFF`
- Yellow: `&H0000FFFF`
- Black: `&H00000000`

### Optimal Worker Count

Calculate optimal workers for your system:

```bash
# macOS/Linux
CORES=$(sysctl -n hw.ncpu 2>/dev/null || nproc)
WORKERS=$((CORES > 2 ? CORES - 1 : 1))
echo "Recommended workers: $WORKERS"
```

### Batch Quality Testing

Test multiple CRF values efficiently:

```bash
for crf in 20 23 26 28; do
  echo "Testing CRF $crf"
  # Edit config programmatically or use config manager
  python main.py --output-suffix "_crf${crf}"
done
```

### Configuration Validation

Validate configuration before running converter:

```python
from src.config import load_config

try:
    config = load_config("config.yaml")
    print("✓ Configuration is valid")
except Exception as e:
    print(f"✗ Configuration error: {e}")
```

## Related Documentation

- [README.md](../README.md) - Project overview and quick start
- [Project Plan](plans/project-plan.md) - Development roadmap
- [config.yaml](../config.yaml) - Configuration file (auto-generated)

## Support & Feedback

If you encounter issues or have suggestions for the config manager:

1. Check this documentation for solutions
2. Review error messages carefully
3. Try resetting to defaults (option 9)
4. Open an issue on GitHub with:
   - Operating system and Python version
   - Error message or unexpected behavior
   - Steps to reproduce
   - Your configuration (if relevant)

---

**Last Updated:** December 6, 2025  
**Version:** 1.0  
**Related Files:** `scripts/config_manager.py`, `src/config.py`, `config.yaml`
