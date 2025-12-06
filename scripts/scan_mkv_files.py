#!/usr/bin/env python3
"""Helper script to scan and display MKV files in the input folder.

This script scans the input directory for MKV files and displays
detailed information about each file including size, path, and
whether it has already been converted.

Usage:
    python scripts/scan_mkv_files.py
    # or
    .venv/bin/python scripts/scan_mkv_files.py

    # With custom config file
    python scripts/scan_mkv_files.py --config custom_config.yaml
"""

import sys
import argparse
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import load_config, Config
from src.converter import BatchConverter
from src.utils import get_video_info, validate_ffprobe
from loguru import logger


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format.

    Args:
        size_bytes: File size in bytes

    Returns:
        str: Formatted file size (e.g., "1.2 GB", "450 MB")
    """
    if size_bytes >= 1024**3:  # GB
        return f"{size_bytes / (1024**3):.2f} GB"
    elif size_bytes >= 1024**2:  # MB
        return f"{size_bytes / (1024**2):.2f} MB"
    elif size_bytes >= 1024:  # KB
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes} B"


def check_already_converted(input_file: Path, converter: BatchConverter) -> bool:
    """Check if a file has already been converted.

    Args:
        input_file: Path to the input MKV file
        converter: BatchConverter instance

    Returns:
        bool: True if output file exists
    """
    output_file = converter._generate_output_path(input_file)
    return output_file.exists()


def display_file_info(mkv_file: Path, converter: BatchConverter, show_details: bool = False) -> None:
    """Display information about a single MKV file.

    Args:
        mkv_file: Path to the MKV file
        converter: BatchConverter instance
        show_details: Whether to show detailed video information
    """
    # Get file size
    size_bytes = mkv_file.stat().st_size
    size_str = format_file_size(size_bytes)

    # Check if already converted
    already_converted = check_already_converted(mkv_file, converter)
    status = "✅ Converted" if already_converted else "⏳ Pending"

    # Display basic info
    print(f"\n  📄 {mkv_file.name}")
    print(f"     Path: {mkv_file}")
    print(f"     Size: {size_str}")
    print(f"     Status: {status}")

    # Display detailed video info if requested
    if show_details and validate_ffprobe():
        video_info = get_video_info(mkv_file)
        if video_info:
            print(f"     Video Details:")
            if "codec_name" in video_info:
                print(f"       - Codec: {video_info['codec_name']}")
            if "width" in video_info and "height" in video_info:
                print(f"       - Resolution: {video_info['width']}x{video_info['height']}")
            if "duration" in video_info:
                duration_sec = float(video_info['duration'])
                duration_min = int(duration_sec // 60)
                duration_sec_remainder = int(duration_sec % 60)
                print(f"       - Duration: {duration_min}m {duration_sec_remainder}s")


def main() -> int:
    """Main entry point for MKV scanning script.

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Scan and display MKV files in the input folder"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)"
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="Show detailed video information (requires ffprobe)"
    )
    args = parser.parse_args()

    print("\n" + "="*60)
    print("              MKV File Scanner")
    print("="*60 + "\n")

    # Configure logger for this script
    logger.remove()
    logger.add(
        sys.stderr,
        format="<level>{level: <8}</level> | <level>{message}</level>",
        level="WARNING"
    )

    # Load configuration
    try:
        config: Config = load_config(args.config)
        print(f"📁 Scanning directory: {config.input_folder}")
        print(f"📁 Output directory: {config.output_folder}")
        print(f"🎬 Target resolution: {config.video.resolution}p")
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return 1

    # Create converter instance
    converter = BatchConverter(config)

    # Scan for MKV files
    print(f"\n🔍 Scanning for MKV files...")
    mkv_files = converter.scan_input_folder()

    if not mkv_files:
        print("\n⚠️  No MKV files found in the input directory.")
        print(f"\n💡 Place your MKV files in: {config.input_folder}")
        return 0

    # Display summary
    total_files = len(mkv_files)
    total_size = sum(f.stat().st_size for f in mkv_files)
    already_converted = sum(1 for f in mkv_files if check_already_converted(f, converter))
    pending = total_files - already_converted

    print(f"\n📊 Summary:")
    print(f"   Total MKV files found: {total_files}")
    print(f"   Already converted: {already_converted}")
    print(f"   Pending conversion: {pending}")
    print(f"   Total size: {format_file_size(total_size)}")

    # Display individual file information
    print(f"\n📋 File List:")
    print("="*60)

    for mkv_file in mkv_files:
        display_file_info(mkv_file, converter, show_details=args.details)

    # Display footer
    print("\n" + "="*60)
    if pending > 0:
        print(f"✨ {pending} file(s) ready for conversion")
        print(f"   Run 'python main.py' to start converting")
    else:
        print("✅ All files have been converted!")
    print("="*60 + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
