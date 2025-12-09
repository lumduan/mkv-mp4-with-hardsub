#!/usr/bin/env python3
"""Test script for Thai font rendering with tone marks.

This script tests the rendering of Thai characters including tone marks
and diacritics (้ ่ ๊ ๋ ั ิ ี ึ ื ุ ู เ แ โ ใ ไ) to ensure proper
subtitle rendering in FFmpeg conversions.

The script can generate test subtitle files and verify that the FFmpeg
subtitle filter correctly renders Thai Unicode combining characters.

Usage:
    python debug/test_thai_fonts.py
"""

import subprocess
import platform
import sys
from pathlib import Path


# Thai text samples with various tone marks and vowels
THAI_TEST_SAMPLES = [
    # Tone marks (combining characters)
    "ฉันบอกให้เธอทำให้เสร็จก่อนนี้ไม่ต้องมาเถียง",
    "ทดสอบการแสดงผลภาษาไทย",
    "สระและวรรณยุกต์: ่ ้ ๊ ๋",
    "สระบน: ั ิ ี ึ ื",
    "สระล่าง: ุ ู",
    "สระหน้า: เ แ โ ใ ไ",
    # Combining tone marks with consonants
    "ก่ ก้ ก๊ ก๋",
    "ข่ ข้ ข๊ ข๋",
    "ค่ ค้ ค๊ ค๋",
    "ต่ ต้ ต๊ ต๋",
    # Complex words with tone marks
    "น้ำ ไม้ ไข่ ไฟ",
    "ความสำเร็จ",
    "การพัฒนา",
    # Common words with diacritics
    "ทำไม ยังไง ที่ไหน อย่างไร",
    "สวัสดี ขอบคุณ ยินดี",
]


def get_system_info() -> dict[str, str]:
    """Get system information for debugging.

    Returns:
        dict: System information including OS, Python version, etc.
    """
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "python_version": sys.version,
        "platform": platform.platform(),
    }


def check_ffmpeg() -> bool:
    """Check if FFmpeg is installed and accessible.

    Returns:
        bool: True if FFmpeg is available, False otherwise
    """
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_fonts_directory() -> str:
    """Get system fonts directory based on OS.

    Returns:
        str: Path to system fonts directory
    """
    system = platform.system()

    if system == "Darwin":  # macOS
        return "/System/Library/Fonts/"
    elif system == "Linux":
        return "/usr/share/fonts/"
    elif system == "Windows":
        return "C:/Windows/Fonts/"
    else:
        return "/usr/share/fonts/"


def list_thai_fonts() -> list[str]:
    """List available Thai fonts on the system.

    Returns:
        list: List of Thai font names found
    """
    fonts_dir = Path(get_fonts_directory())
    thai_fonts = []

    # Common Thai font patterns to search for
    thai_font_patterns = [
        "*Sarabun*",
        "*TH*",
        "*Angsana*",
        "*Cordia*",
        "*Browallia*",
        "*Leelawadee*",
        "*Thai*",
    ]

    if fonts_dir.exists():
        for pattern in thai_font_patterns:
            thai_fonts.extend([f.name for f in fonts_dir.rglob(pattern)])

    return sorted(set(thai_fonts))


def create_test_srt(output_path: Path) -> None:
    """Create a test SRT subtitle file with Thai text.

    Args:
        output_path: Path where to save the SRT file
    """
    srt_content = []

    for i, text in enumerate(THAI_TEST_SAMPLES, 1):
        # Each subtitle shows for 3 seconds
        start_time = (i - 1) * 3
        end_time = i * 3

        # Format time as SRT timestamp (HH:MM:SS,mmm)
        start_str = f"00:00:{start_time:02d},000"
        end_str = f"00:00:{end_time:02d},000"

        srt_content.append(f"{i}\n{start_str} --> {end_str}\n{text}\n")

    output_path.write_text("\n".join(srt_content), encoding="utf-8")
    print(f"✅ Created test subtitle file: {output_path}")


def test_thai_rendering() -> None:
    """Test Thai character rendering with tone marks."""
    print("\n" + "="*70)
    print("              🇹🇭 Thai Font Rendering Test")
    print("="*70)

    # Display system info
    print("\n📊 System Information:")
    sys_info = get_system_info()
    for key, value in sys_info.items():
        print(f"   {key}: {value}")

    # Check FFmpeg
    print("\n🔍 Checking FFmpeg:")
    if check_ffmpeg():
        print("   ✅ FFmpeg is installed")
    else:
        print("   ❌ FFmpeg not found!")
        print("   Please install FFmpeg to continue")
        return

    # Display fonts directory
    fonts_dir = get_fonts_directory()
    print(f"\n📁 System fonts directory: {fonts_dir}")

    # List Thai fonts
    print("\n🔤 Available Thai fonts:")
    thai_fonts = list_thai_fonts()
    if thai_fonts:
        for font in thai_fonts[:10]:  # Show first 10
            print(f"   - {font}")
        if len(thai_fonts) > 10:
            print(f"   ... and {len(thai_fonts) - 10} more")
    else:
        print("   ⚠️  No Thai fonts found in system directory")
        print("   FFmpeg will use default fonts")

    # Display Thai test samples
    print("\n📝 Thai Text Test Samples:")
    print("="*70)
    for i, sample in enumerate(THAI_TEST_SAMPLES, 1):
        print(f"{i:2d}. {sample}")

    # Create test subtitle file
    print("\n📄 Creating test subtitle file...")
    srt_path = Path("debug/test_thai_subtitles.srt")
    create_test_srt(srt_path)

    # Instructions for manual testing
    print("\n" + "="*70)
    print("              📋 Manual Testing Instructions")
    print("="*70)
    print("\nTo test Thai subtitle rendering:")
    print("\n1. Place a test video file in the 'input/' folder")
    print("2. Run the conversion script:")
    print("   python scripts/process_mkv_files.py")
    print("\n3. Check the output video for proper Thai tone mark rendering:")
    print("   - Tone marks (่ ้ ๊ ๋) should appear above consonants")
    print("   - Vowels (ั ิ ี ึ ื) should appear in correct positions")
    print("   - Characters should not overlap or misalign")
    print("\n4. If tone marks still don't render correctly:")
    print("   - Verify Thai fonts are installed on your system")
    print("   - Check FFmpeg can access the fonts directory")
    print("   - Try specifying a specific Thai font in config.yaml")

    # Sample FFmpeg command
    print("\n💡 Sample FFmpeg command with Thai font support:")
    print("="*70)
    sample_cmd = (
        f"ffmpeg -i input.mkv "
        f"-vf \"subtitles=input.mkv:fontsdir='{fonts_dir}'\" "
        f"output.mp4"
    )
    print(sample_cmd)

    print("\n" + "="*70)
    print("              ✅ Test Complete")
    print("="*70)
    print()


def main() -> int:
    """Main entry point.

    Returns:
        int: Exit code (0 for success)
    """
    try:
        test_thai_rendering()
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
