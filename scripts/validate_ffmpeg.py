#!/usr/bin/env python3
"""Helper script to validate FFmpeg installation.

This script checks if FFmpeg and FFprobe are properly installed
and accessible in the system PATH. It provides detailed information
about the FFmpeg installation including version, capabilities, and codecs.

Usage:
    python scripts/validate_ffmpeg.py
    # or
    .venv/bin/python scripts/validate_ffmpeg.py
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import validate_ffmpeg, get_ffmpeg_version, validate_ffprobe
from loguru import logger
import subprocess


def check_ffmpeg_codecs() -> dict[str, bool]:
    """Check if required codecs are available in FFmpeg.

    Returns:
        dict[str, bool]: Dictionary mapping codec names to availability
    """
    required_codecs = {
        "libx264": False,
        "libx265": False,
        "aac": False,
    }

    try:
        # Get list of available encoders
        result = subprocess.run(
            ["ffmpeg", "-encoders"],
            capture_output=True,
            text=True,
            timeout=10
        )

        output = result.stdout.lower()

        # Check each required codec
        for codec in required_codecs.keys():
            if codec.lower() in output:
                required_codecs[codec] = True

        return required_codecs
    except Exception as e:
        logger.error(f"Failed to check FFmpeg codecs: {e}")
        return required_codecs


def check_subtitle_support() -> bool:
    """Check if FFmpeg has subtitle filter support.

    Returns:
        bool: True if subtitle filter is available
    """
    try:
        result = subprocess.run(
            ["ffmpeg", "-filters"],
            capture_output=True,
            text=True,
            timeout=10
        )

        return "subtitles" in result.stdout.lower()
    except Exception:
        return False


def main() -> int:
    """Main entry point for FFmpeg validation script.

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    print("\n" + "="*60)
    print("           FFmpeg Installation Validator")
    print("="*60 + "\n")

    # Configure logger for this script
    logger.remove()
    logger.add(sys.stderr, format="<level>{level: <8}</level> | <level>{message}</level>", level="INFO")

    # Step 1: Check FFmpeg
    print("🔍 Checking FFmpeg installation...")
    if validate_ffmpeg():
        version = get_ffmpeg_version()
        print(f"✅ FFmpeg is installed")
        if version:
            print(f"   Version: {version}")
    else:
        print("❌ FFmpeg is NOT installed or not accessible")
        print("\n💡 Installation instructions:")
        print("   macOS:    brew install ffmpeg")
        print("   Ubuntu:   sudo apt install ffmpeg")
        print("   Windows:  choco install ffmpeg")
        return 1

    # Step 2: Check FFprobe
    print("\n🔍 Checking FFprobe installation...")
    if validate_ffprobe():
        print("✅ FFprobe is installed")
    else:
        print("⚠️  FFprobe is NOT installed (optional but recommended)")

    # Step 3: Check required codecs
    print("\n🔍 Checking required codecs...")
    codecs = check_ffmpeg_codecs()

    all_codecs_available = True
    for codec, available in codecs.items():
        status = "✅" if available else "❌"
        print(f"{status} {codec}: {'Available' if available else 'NOT Available'}")
        if not available:
            all_codecs_available = False

    if not all_codecs_available:
        print("\n⚠️  Some required codecs are missing!")
        print("   You may need to reinstall FFmpeg with full codec support.")
        return 1

    # Step 4: Check subtitle support
    print("\n🔍 Checking subtitle filter support...")
    if check_subtitle_support():
        print("✅ Subtitle filter is available")
    else:
        print("⚠️  Subtitle filter is NOT available")
        print("   Hard-coded subtitles may not work properly.")
        return 1

    # Final summary
    print("\n" + "="*60)
    print("✅ All checks passed! FFmpeg is properly configured.")
    print("="*60 + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
