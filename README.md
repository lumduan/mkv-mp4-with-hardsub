# 🎬 MKV to MP4 Batch Converter with Hard-Sub

A powerful Python-based batch conversion tool that converts MKV files to 480p MP4 with hard-coded subtitles using FFmpeg. Features comprehensive YAML-based configuration management and an interactive CLI for easy setup.

## ✨ Features

- **Batch Processing**: Convert multiple MKV files in one run
- **Hard-Coded Subtitles**: Burn subtitles directly into the video
- **Flexible Configuration**: YAML-based configuration with validation
- **Interactive Config Manager**: Menu-driven CLI for easy settings management
- **Quality Control**: Configurable resolution, codecs, and quality settings
- **Parallel Processing**: Optional multi-threaded conversion (experimental)
- **Smart Skip**: Automatically skip already converted files
- **Comprehensive Logging**: Detailed logs with success/error tracking using Loguru
- **Type-Safe**: Full Pydantic validation for all settings

## 📋 Requirements

### System Requirements
- **FFmpeg**: Must be installed and accessible in PATH
- **Python**: 3.10 or higher
- **Disk Space**: Sufficient for input and output files
- **CPU**: Multi-core recommended for parallel processing

### Installing FFmpeg

**macOS** (using Homebrew):
```bash
brew install ffmpeg
```

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows** (using Chocolatey):
```bash
choco install ffmpeg
```

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/mkv-mp4-with-hardsub.git
cd mkv-mp4-with-hardsub
```

### 2. Install Dependencies

Using `uv` (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
```

### 3. Configure Settings

**Option A: Use the Interactive Config Manager** (Recommended)
```bash
.venv/bin/python scripts/config_manager.py
```

This launches an interactive menu with:
- **Quick Setup Wizard**: Easy step-by-step configuration for first-time users
- **Guided Quality Presets**: Choose from High Quality, Balanced, or Smaller Files
- **Smart Defaults**: Automatically configure optimal settings
- **Real-time Validation**: Validates all inputs before saving
- **Help System**: Built-in documentation with detailed explanations

**Option B: Edit `config.yaml` Directly**
```bash
nano config.yaml  # or your preferred editor
```

### 4. Add MKV Files
Place your MKV files in the `input/` folder:
```bash
cp /path/to/your/videos/*.mkv input/
```

### 5. Run the Converter

**Option A: Interactive Menu-Driven Processor** (Recommended)
```bash
.venv/bin/python scripts/process_mkv_files.py
```

This launches an interactive menu with:
- **View files and status**: See all MKV files with conversion status
- **Process single file**: Convert one file at a time with progress feedback
- **Batch process all files**: Convert all pending files automatically
- **Conversion history**: Track results from current session
- **Real-time progress**: See detailed conversion statistics

**Option B: Direct Script Execution**
```bash
python main.py
```

Converted files will appear in the `output/` folder with the `_480p.mp4` suffix.

## ⚙️ Configuration Guide

### YAML Configuration Structure

The `config.yaml` file contains all settings for the converter:

```yaml
# Directory Settings
input_folder: "input"       # Source MKV files
output_folder: "output"     # Converted MP4 files
logs_folder: "logs"         # Log files

# Video Encoding Settings
video:
  resolution: 480           # Target height in pixels
  codec: "libx264"          # Video codec (libx264, libx265)
  crf: 24                   # Quality (0-51, lower = better)
  preset: "medium"          # Speed preset

# Audio Encoding Settings
audio:
  codec: "aac"              # Audio codec
  bitrate: "128k"           # Audio bitrate

# Subtitle Settings
subtitles:
  enabled: true             # Enable subtitle burning
  language: null            # Preferred language (e.g., "eng")
  force_style: null         # Custom subtitle styling

# Processing Options
parallel_processing: false  # Enable parallel conversion
max_workers: 2              # Number of parallel workers
skip_existing: true         # Skip already converted files
verbose: false              # Enable debug logging
```

### Configuration Options Explained

#### Video Settings

| Setting | Description | Valid Values | Default |
|---------|-------------|--------------|---------|
| `resolution` | Target video height | 144-2160 | 480 |
| `codec` | Video encoder | libx264, libx265, h264, hevc | libx264 |
| `crf` | Quality level (lower = better) | 0-51 | 24 |
| `preset` | Encoding speed | ultrafast to veryslow | medium |

**CRF Quality Guide:**
- **18-20**: High quality, large files (near lossless)
- **23-24**: Good quality, balanced size (recommended)
- **28-30**: Lower quality, smaller files

**Preset Speed Guide:**
- **ultrafast**: Fastest, largest files
- **medium**: Balanced (default)
- **veryslow**: Slowest, best compression

#### Audio Settings

| Setting | Description | Valid Values | Default |
|---------|-------------|--------------|---------|
| `codec` | Audio encoder | aac, mp3, opus, ac3 | aac |
| `bitrate` | Audio quality | 96k, 128k, 192k, 256k | 128k |

#### Processing Options

| Setting | Description | Type | Default |
|---------|-------------|------|---------|
| `parallel_processing` | Convert multiple files simultaneously | boolean | false |
| `max_workers` | Number of parallel workers | 1-16 | 2 |
| `skip_existing` | Skip files already converted | boolean | true |
| `verbose` | Show debug information | boolean | false |

### Environment Variables

All settings can be overridden with environment variables using the `CONVERTER_` prefix:

```bash
# Example: Override video resolution
export CONVERTER_VIDEO__RESOLUTION=720

# Example: Enable verbose mode
export CONVERTER_VERBOSE=true

# Run the converter
python main.py
```

## 🛠️ Utility Scripts

The project includes several interactive menu-driven scripts to help with different tasks:

### 1. Interactive MKV Processor (process_mkv_files.py)

**Purpose**: Process MKV files with an interactive menu interface (implements Step 4 of the project plan)

```bash
.venv/bin/python scripts/process_mkv_files.py
```

**Features**:
- **View Files**: Browse all MKV files with conversion status and file details
- **Single File Processing**: Convert individual files with real-time progress
- **Batch Processing**: Convert all pending files automatically
- **Detailed Feedback**: See file size reduction, conversion time, and quality metrics
- **Conversion History**: Track all conversions in the current session
- **Error Handling**: Graceful error reporting with retry options
- **Progress Tracking**: Real-time conversion statistics and summaries

**Example Workflow**:
```text
📋 Main Menu:
  1. View files and status
  2. View files with details (requires ffprobe)
  3. Process single file
  4. 🚀 Process all pending files
  5. View conversion history (current session)
  6. View current settings
  7. Refresh file list
  H. Show help
  0. Exit
```

### 2. Interactive Config Manager (config_manager.py)

**Purpose**: Manage configuration settings with a user-friendly interface

The config manager provides a user-friendly menu-driven interface for managing settings with an enhanced Quick Setup Wizard for first-time users.

### Launch the Config Manager

```bash
.venv/bin/python scripts/config_manager.py
```

### Features

#### 🚀 Quick Setup Wizard (New!)
Perfect for first-time users or quick reconfiguration:
- **Quality Presets**: Choose from 3 optimized presets:
  - High Quality (720p, CRF 20) - Better quality, larger files
  - Balanced (480p, CRF 24) - Recommended for most users
  - Smaller Files (480p, CRF 28) - Faster conversion, smaller files
- **Guided Subtitle Configuration**: Enable/disable and select language
- **Performance Options**: Configure parallel processing
- **Directory Setup**: Configure input/output paths

#### 📋 Advanced Configuration Menu
- **View Configuration**: Display all current settings in organized sections
- **Update Settings by Category**:
  - Directory paths
  - Video encoding options
  - Audio encoding options
  - Subtitle settings
  - Processing options
- **Help System (Press H)**: Detailed documentation with:
  - Video settings explained (resolution, CRF, codec, preset)
  - Audio codec recommendations
  - Common quality presets
  - File location information
- **Save/Reload**: Save changes or reload from disk
- **Reset to Defaults**: Restore factory settings
- **Real-time Validation**: Validates all inputs before accepting changes

### Example Usage - Quick Setup Wizard

```text
======================================================================
               🎬 MKV to MP4 Converter
               Configuration Manager
======================================================================

📝 About config.yaml:
   The config.yaml file controls how your videos are converted.

🎯 It looks like this is your first time setting up.
Would you like to run the Quick Setup Wizard? (yes/no) [yes]: yes

======================================================================
🚀 Quick Setup Wizard
======================================================================

📊 Choose quality preset:
  1. High Quality (720p, CRF 20) - Larger files, better quality
  2. Balanced (480p, CRF 24) - Recommended for most users
  3. Smaller Files (480p, CRF 28) - Faster conversion, smaller files

Select preset (1-3) [2]: 2
✓ Balanced preset selected

📝 Subtitle settings:
Do you want to burn subtitles into the video? (yes/no) [yes]: yes
Preferred subtitle language code (e.g., eng, tha, jpn) [auto]: eng
✓ Will use 'eng' subtitles when available

⚙️  Performance settings:
Enable parallel processing for faster conversion? (yes/no) [no]: no

📁 Directory settings:
Use default folders (input/, output/)? (yes/no) [yes]: yes

✨ Setup complete! Your configuration:
[Shows current configuration]

💾 Save this configuration to config.yaml? (yes/no) [yes]: yes
✓ Configuration saved to config.yaml

✅ Configuration saved! You can now run the converter.
   To make changes later, run this script again.
```

### Example Usage - Advanced Menu

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

Select option: 4

🎬 Video Encoding Settings
----------------------------------------
Resolution (144-2160) [480]: 720
Available codecs: libx264, libx265, h264, hevc
Video codec [libx264]: libx264
CRF quality (0-51, lower=better) [24]: 23
Available presets: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
Encoding preset [medium]: slow
✓ Video settings updated

Select option: 8
✓ Configuration saved to config.yaml
```

## 📁 Project Structure

```
mkv-mp4-with-hardsub/
│
├── input/              # Source MKV files (not tracked in git)
├── output/             # Converted MP4 files (not tracked in git)
├── logs/               # Processing logs
│
├── src/                # Source code
│   ├── __init__.py
│   ├── config.py       # YAML configuration management
│   ├── converter.py    # Core conversion logic
│   ├── logger.py       # Logging utilities
│   └── utils.py        # Helper functions
│
├── scripts/            # Utility scripts
│   ├── __init__.py
│   ├── config_manager.py     # Interactive config manager
│   ├── process_mkv_files.py  # Interactive MKV processor (Step 4)
│   ├── scan_mkv_files.py     # MKV file scanner
│   └── validate_ffmpeg.py    # FFmpeg validation
│
├── tests/              # Unit tests
│   ├── test_converter.py
│   ├── test_config.py
│   └── test_utils.py
│
├── docs/               # Documentation
│   └── plans/
│       └── project-plan.md
│
├── config.yaml         # Main configuration file
├── main.py             # Entry point
├── pyproject.toml      # Python dependencies
├── README.md           # This file
└── .gitignore
```

## 📊 Usage Examples

### Basic Conversion
```bash
# 1. Place MKV files in input folder
cp ~/Videos/*.mkv input/

# 2. Run converter
python main.py

# 3. Find converted files in output/
ls -lh output/
```

### Custom Configuration
```bash
# Create a custom config
cp config.yaml config.custom.yaml

# Edit settings
nano config.custom.yaml

# Use custom config (if supported in future version)
python main.py --config config.custom.yaml
```

### Parallel Processing (Experimental)
```bash
# Enable in config.yaml
sed -i '' 's/parallel_processing: false/parallel_processing: true/' config.yaml

# Set worker count to CPU cores - 1
sed -i '' 's/max_workers: 2/max_workers: 7/' config.yaml

# Run converter
python main.py
```

## 🧪 Testing

Run unit tests:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=src tests/
```

## 📝 Logging

The converter generates detailed logs in the `logs/` folder:

- **conversion_YYYY-MM-DD.log**: Daily log with all operations
- **success.log**: Only successful conversions
- **errors.log**: Only failures with full tracebacks

### Log Example
```
2025-12-06 15:30:45 | INFO     | Configuration loaded successfully
2025-12-06 15:30:46 | INFO     | Found 5 MKV file(s) to process
2025-12-06 15:30:47 | SUCCESS  | movie1.mkv → movie1_480p.mp4 | 1200.5MB → 450.2MB | 145.3s
2025-12-06 15:33:12 | SUCCESS  | movie2.mkv → movie2_480p.mp4 | 1500.8MB → 520.1MB | 178.6s
2025-12-06 15:36:05 | ERROR    | corrupted.mkv - FFmpeg error: Invalid data found
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **FFmpeg**: The powerful multimedia framework that makes this possible
- **Pydantic**: For robust configuration validation
- **Loguru**: For beautiful and functional logging
- **PyYAML**: For YAML parsing and serialization

## 🐛 Troubleshooting

### FFmpeg Not Found
```bash
# Check FFmpeg installation
ffmpeg -version

# If not found, install it (see Requirements section)
```

### Permission Denied
```bash
# Make sure directories are writable
chmod 755 input output logs

# Or use sudo (not recommended)
sudo python main.py
```

### Configuration Errors
```bash
# Validate your YAML syntax
python -c "import yaml; yaml.safe_load(open('config.yaml'))"

# Reset to defaults
python scripts/config_manager.py
# Then select option 8 (Reset to defaults)
```

### Out of Disk Space
```bash
# Check available space
df -h

# Clean up old conversions
rm output/*_480p.mp4
```

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the project plan in `docs/plans/project-plan.md`

## 🗺️ Roadmap

- [ ] Web-based configuration interface
- [ ] Watch folder mode for automatic conversion
- [ ] GPU acceleration support
- [ ] Batch subtitle track selection
- [ ] HTML report generation
- [ ] Docker containerization
- [ ] REST API for remote conversion

---

**Made with ❤️ using Python, FFmpeg, and YAML**
