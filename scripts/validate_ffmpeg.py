#!/usr/bin/env python3
"""Helper script to validate FFmpeg installation.

This script checks if FFmpeg and FFprobe are properly installed
and accessible in the system PATH. It provides detailed information
about the FFmpeg installation including version, capabilities, and codecs.

Features:
- OS detection (macOS, Linux, Windows)
- Platform-specific installation instructions
- Optional automatic FFmpeg installation
- Comprehensive validation checks

Usage:
    python scripts/validate_ffmpeg.py
    # or
    .venv/bin/python scripts/validate_ffmpeg.py

    # With automatic installation (requires sudo/admin on some platforms)
    python scripts/validate_ffmpeg.py --install
"""

import sys
import platform
import shutil
from pathlib import Path
from typing import Optional, Tuple

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


def detect_os() -> Tuple[str, str]:
    """Detect the operating system.

    Returns:
        Tuple[str, str]: (os_type, os_name) where os_type is one of:
            'darwin' (macOS), 'linux', 'windows', 'unknown'
    """
    system = platform.system().lower()
    os_name = platform.platform()

    if system == 'darwin':
        return 'darwin', f"macOS {platform.mac_ver()[0]}"
    elif system == 'linux':
        # Try to get Linux distribution info
        try:
            import distro
            dist_name = distro.name(pretty=True)
            return 'linux', dist_name
        except ImportError:
            return 'linux', os_name
    elif system == 'windows':
        return 'windows', os_name
    else:
        return 'unknown', os_name


def check_package_manager() -> Optional[str]:
    """Check which package manager is available.

    Returns:
        Optional[str]: Package manager name ('brew', 'apt', 'yum', 'dnf', 'pacman', 'choco', etc.)
    """
    package_managers = {
        'brew': '/usr/local/bin/brew',  # macOS Homebrew
        'apt': '/usr/bin/apt',          # Debian/Ubuntu
        'apt-get': '/usr/bin/apt-get',  # Debian/Ubuntu (older)
        'yum': '/usr/bin/yum',          # RHEL/CentOS
        'dnf': '/usr/bin/dnf',          # Fedora
        'pacman': '/usr/bin/pacman',    # Arch Linux
        'choco': 'C:\\ProgramData\\chocolatey\\bin\\choco.exe',  # Windows Chocolatey
    }

    for pm_name, pm_path in package_managers.items():
        # Check using shutil.which for cross-platform compatibility
        if shutil.which(pm_name):
            return pm_name

    return None


def get_installation_instructions(os_type: str, package_manager: Optional[str] = None) -> dict[str, str]:
    """Get installation instructions for the detected OS.

    Args:
        os_type: Operating system type ('darwin', 'linux', 'windows', 'unknown')
        package_manager: Detected package manager (optional)

    Returns:
        dict[str, str]: Dictionary with installation methods
    """
    instructions = {}

    if os_type == 'darwin':
        instructions['homebrew'] = "brew install ffmpeg"
        instructions['macports'] = "sudo port install ffmpeg"
        instructions['manual'] = "Download from: https://evermeet.cx/ffmpeg/"

    elif os_type == 'linux':
        if package_manager == 'apt' or package_manager == 'apt-get':
            instructions['apt'] = "sudo apt update && sudo apt install ffmpeg"
        elif package_manager == 'yum':
            instructions['yum'] = "sudo yum install ffmpeg"
        elif package_manager == 'dnf':
            instructions['dnf'] = "sudo dnf install ffmpeg"
        elif package_manager == 'pacman':
            instructions['pacman'] = "sudo pacman -S ffmpeg"
        else:
            instructions['generic'] = "Use your distribution's package manager to install ffmpeg"
        instructions['snap'] = "sudo snap install ffmpeg"
        instructions['manual'] = "Download from: https://ffmpeg.org/download.html#build-linux"

    elif os_type == 'windows':
        if package_manager == 'choco':
            instructions['chocolatey'] = "choco install ffmpeg"
        instructions['scoop'] = "scoop install ffmpeg"
        instructions['winget'] = "winget install ffmpeg"
        instructions['manual'] = "Download from: https://ffmpeg.org/download.html#build-windows"

    else:
        instructions['manual'] = "Visit https://ffmpeg.org/download.html for installation instructions"

    return instructions


def install_ffmpeg_auto(os_type: str, package_manager: Optional[str]) -> bool:
    """Attempt to automatically install FFmpeg.

    Args:
        os_type: Operating system type
        package_manager: Detected package manager

    Returns:
        bool: True if installation was successful
    """
    print("\n🔧 Attempting to install FFmpeg automatically...")

    try:
        if os_type == 'darwin' and package_manager == 'brew':
            print("   Using Homebrew to install FFmpeg...")
            result = subprocess.run(
                ["brew", "install", "ffmpeg"],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            if result.returncode == 0:
                print("✅ FFmpeg installed successfully via Homebrew!")
                return True
            else:
                print(f"❌ Installation failed: {result.stderr}")
                return False

        elif os_type == 'linux':
            if package_manager in ['apt', 'apt-get']:
                print("   Using apt to install FFmpeg (requires sudo)...")
                # Update package list
                subprocess.run(["sudo", "apt", "update"], check=True, timeout=60)
                # Install ffmpeg
                result = subprocess.run(
                    ["sudo", "apt", "install", "-y", "ffmpeg"],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                if result.returncode == 0:
                    print("✅ FFmpeg installed successfully via apt!")
                    return True
                else:
                    print(f"❌ Installation failed: {result.stderr}")
                    return False

            elif package_manager == 'dnf':
                print("   Using dnf to install FFmpeg (requires sudo)...")
                result = subprocess.run(
                    ["sudo", "dnf", "install", "-y", "ffmpeg"],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                if result.returncode == 0:
                    print("✅ FFmpeg installed successfully via dnf!")
                    return True
                else:
                    print(f"❌ Installation failed: {result.stderr}")
                    return False

            elif package_manager == 'yum':
                print("   Using yum to install FFmpeg (requires sudo)...")
                result = subprocess.run(
                    ["sudo", "yum", "install", "-y", "ffmpeg"],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                if result.returncode == 0:
                    print("✅ FFmpeg installed successfully via yum!")
                    return True
                else:
                    print(f"❌ Installation failed: {result.stderr}")
                    return False

            elif package_manager == 'pacman':
                print("   Using pacman to install FFmpeg (requires sudo)...")
                result = subprocess.run(
                    ["sudo", "pacman", "-S", "--noconfirm", "ffmpeg"],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                if result.returncode == 0:
                    print("✅ FFmpeg installed successfully via pacman!")
                    return True
                else:
                    print(f"❌ Installation failed: {result.stderr}")
                    return False

        elif os_type == 'windows' and package_manager == 'choco':
            print("   Using Chocolatey to install FFmpeg (requires admin)...")
            result = subprocess.run(
                ["choco", "install", "-y", "ffmpeg"],
                capture_output=True,
                text=True,
                timeout=300,
                shell=True  # Windows requires shell=True
            )
            if result.returncode == 0:
                print("✅ FFmpeg installed successfully via Chocolatey!")
                return True
            else:
                print(f"❌ Installation failed: {result.stderr}")
                return False

        print("⚠️  Automatic installation not supported for your system.")
        print("   Please install FFmpeg manually using the instructions above.")
        return False

    except subprocess.TimeoutExpired:
        print("❌ Installation timed out. Please try installing manually.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during installation: {e}")
        return False


def main() -> int:
    """Main entry point for FFmpeg validation script.

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Validate and install FFmpeg")
    parser.add_argument(
        '--install',
        action='store_true',
        help="Attempt to install FFmpeg automatically"
    )
    args = parser.parse_args()

    print("\n" + "="*60)
    print("           FFmpeg Installation Validator")
    print("="*60 + "\n")

    # Configure logger for this script
    logger.remove()
    logger.add(sys.stderr, format="<level>{level: <8}</level> | <level>{message}</level>", level="INFO")

    # Detect OS and package manager
    os_type, os_name = detect_os()
    package_manager = check_package_manager()

    print(f"🖥️  Detected OS: {os_name}")
    if package_manager:
        print(f"📦 Package Manager: {package_manager}")
    else:
        print(f"📦 Package Manager: Not detected")
    print()

    # Step 1: Check FFmpeg
    print("🔍 Checking FFmpeg installation...")
    ffmpeg_installed = validate_ffmpeg()

    if ffmpeg_installed:
        version = get_ffmpeg_version()
        print(f"✅ FFmpeg is installed")
        if version:
            print(f"   Version: {version}")
    else:
        print("❌ FFmpeg is NOT installed or not accessible")

        # Get installation instructions
        instructions = get_installation_instructions(os_type, package_manager)

        if args.install:
            # Attempt automatic installation
            if package_manager:
                print(f"\n💡 Automatic installation is available for your system.")
                response = input("   Do you want to install FFmpeg now? (yes/no): ").lower().strip()

                if response in ['yes', 'y']:
                    if install_ffmpeg_auto(os_type, package_manager):
                        # Verify installation
                        print("\n🔍 Verifying installation...")
                        if validate_ffmpeg():
                            print("✅ FFmpeg is now installed and working!")
                            ffmpeg_installed = True
                        else:
                            print("⚠️  Installation completed but FFmpeg is not accessible.")
                            print("   You may need to restart your terminal or update your PATH.")
                            return 1
                    else:
                        print("\n⚠️  Automatic installation failed.")
                        print("   Please try manual installation using the instructions below.")
                else:
                    print("\n⚠️  Installation cancelled.")
            else:
                print("\n⚠️  Automatic installation is not available for your system.")
                print("   Please install FFmpeg manually using the instructions below.")

        # Show installation instructions
        if not ffmpeg_installed:
            print("\n💡 Installation instructions for your system:")
            print("="*60)
            for method, command in instructions.items():
                print(f"\n{method.upper()}:")
                print(f"   {command}")
            print("\n" + "="*60)

            if not args.install:
                print("\n💡 TIP: Run this script with --install to attempt automatic installation:")
                print(f"   python {sys.argv[0]} --install")

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
