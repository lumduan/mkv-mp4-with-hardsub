"""Helper utilities for video processing."""

import subprocess
from pathlib import Path
from typing import Optional
from loguru import logger


def validate_ffmpeg() -> bool:
    """Check if FFmpeg is installed and accessible.

    Returns:
        bool: True if FFmpeg is installed and working, False otherwise
    """
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )

        # Extract FFmpeg version from output
        version_line = result.stdout.split('\n')[0]
        logger.info(f"FFmpeg found: {version_line}")

        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg command failed: {e.stderr}")
        return False
    except FileNotFoundError:
        logger.error("FFmpeg not found in system PATH")
        return False
    except subprocess.TimeoutExpired:
        logger.error("FFmpeg command timed out")
        return False
    except Exception as e:
        logger.error(f"Unexpected error validating FFmpeg: {e}")
        return False


def get_ffmpeg_version() -> Optional[str]:
    """Get FFmpeg version string.

    Returns:
        Optional[str]: FFmpeg version string or None if not found
    """
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )

        # Extract version from first line
        version_line = result.stdout.split('\n')[0]
        return version_line
    except Exception:
        return None


def validate_ffprobe() -> bool:
    """Check if FFprobe is installed and accessible.

    Returns:
        bool: True if FFprobe is installed and working, False otherwise
    """
    try:
        result = subprocess.run(
            ["ffprobe", "-version"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )

        logger.info("FFprobe found and validated")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        logger.warning("FFprobe not found or not working")
        return False


def get_video_info(video_path: Path) -> dict[str, str]:
    """Extract video metadata using ffprobe.

    Args:
        video_path: Path to the video file

    Returns:
        dict[str, str]: Dictionary containing video metadata
    """
    try:
        cmd: list[str] = [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,codec_name,duration",
            "-of", "default=noprint_wrappers=1",
            str(video_path)
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )

        # Parse output
        info: dict[str, str] = {}
        for line in result.stdout.split("\n"):
            if "=" in line:
                key, value = line.split("=", 1)
                info[key] = value

        return info
    except Exception as e:
        logger.error(f"Failed to get video info for {video_path}: {e}")
        return {}
