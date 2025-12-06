#!/usr/bin/env python3
"""Interactive CLI tool for processing MKV files to MP4 with hard-sub.

This script provides a comprehensive menu-driven interface for Step 4:
Process Each MKV File with the following features:
- View and browse MKV files ready for conversion
- Process individual files with progress feedback
- Batch process all pending files
- View conversion results and statistics
- Customize processing options interactively

Usage:
    python scripts/process_mkv_files.py
    # or
    chmod +x scripts/process_mkv_files.py
    ./scripts/process_mkv_files.py

    # With custom config file
    python scripts/process_mkv_files.py --config custom_config.yaml
"""

import sys
import argparse
from pathlib import Path
from typing import Optional
from datetime import datetime

# Add parent directory to path to import src modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Check Python version and warn about unstable versions
if sys.version_info >= (3, 14) and "a" in sys.version.lower():
    print("\n⚠️  WARNING: You are using Python 3.14 alpha version!")
    print("   This may cause crashes with some dependencies.")
    print("   Recommended: Use Python 3.10, 3.11, 3.12, or 3.13 stable release.\n")
    response = input("Continue anyway? (yes/no) [no]: ").strip().lower()
    if response not in ['yes', 'y']:
        print("Exiting. Please use a stable Python version.")
        sys.exit(1)

try:
    from src.config import load_config, Config
    from src.converter import BatchConverter, ConversionResult
    from src.utils import validate_ffmpeg, get_video_info, validate_ffprobe
    from loguru import logger
except Exception as e:
    print(f"\n❌ Error loading required modules: {e}")
    print("\nPossible solutions:")
    print("  1. Install dependencies: uv sync")
    print("  2. Use a stable Python version (3.10-3.13)")
    print("  3. Check if all dependencies are installed correctly")
    sys.exit(1)


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format.

    Args:
        size_bytes: File size in bytes

    Returns:
        str: Formatted file size (e.g., "1.2 GB", "450 MB")

    Example:
        >>> format_file_size(1536000000)
        '1.43 GB'
    """
    if size_bytes >= 1024**3:  # GB
        return f"{size_bytes / (1024**3):.2f} GB"
    elif size_bytes >= 1024**2:  # MB
        return f"{size_bytes / (1024**2):.2f} MB"
    elif size_bytes >= 1024:  # KB
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes} B"


class MKVProcessor:
    """Interactive MKV file processor with menu-driven interface.

    This class provides a comprehensive CLI interface for processing MKV files
    to MP4 format with hard-coded subtitles. It handles file selection,
    conversion progress, and result reporting.

    Attributes:
        config: Configuration object with conversion settings
        converter: BatchConverter instance for file processing
        mkv_files: List of discovered MKV files
        conversion_history: List of completed conversion results
    """

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize the MKV processor.

        Args:
            config_path: Path to the configuration file
        """
        self.config_path: Path = Path(config_path)
        self.config: Optional[Config] = None
        self.converter: Optional[BatchConverter] = None
        self.mkv_files: list[Path] = []
        self.conversion_history: list[ConversionResult] = []

        # Initialize configuration
        self._load_configuration()

        # Setup logging
        self._setup_logging()

    def _load_configuration(self) -> None:
        """Load configuration and initialize converter."""
        try:
            self.config = load_config(self.config_path)
            logger.info(f"Configuration loaded from {self.config_path}")

            # Ensure required directories exist
            self.config.ensure_directories()

            # Initialize converter
            self.converter = BatchConverter(config=self.config)

        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            print("   Using default configuration")
            self.config = Config()
            self.config.ensure_directories()
            self.converter = BatchConverter(config=self.config)

    def _setup_logging(self) -> None:
        """Setup Loguru logging configuration.

        Configures console and file logging with appropriate levels
        based on the verbose setting in configuration.
        """
        # Remove default handler
        logger.remove()

        # Console handler with color and formatting
        log_level: str = "DEBUG" if self.config.verbose else "INFO"
        logger.add(
            sys.stderr,
            format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
            level=log_level,
            colorize=True,
        )

        # File handler - all logs with rotation
        logger.add(
            self.config.logs_folder / "process_mkv_{time:YYYY-MM-DD}.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
            level="DEBUG",
            rotation="00:00",  # New file at midnight
            retention="30 days",  # Keep logs for 30 days
            compression="zip",  # Compress rotated logs
        )

        # Success log - only successful conversions
        logger.add(
            self.config.logs_folder / "success.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {message}",
            level="SUCCESS",
            filter=lambda record: record["level"].name == "SUCCESS",
        )

        # Error log - only errors
        logger.add(
            self.config.logs_folder / "errors.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            level="ERROR",
            backtrace=True,  # Include full traceback
            diagnose=True,   # Show variable values
        )

        logger.info("Logging initialized for MKV processor")

    def _scan_files(self) -> None:
        """Scan input folder for MKV files."""
        logger.info(f"Scanning {self.config.input_folder} for MKV files...")
        self.mkv_files = self.converter.scan_input_folder()

        if not self.mkv_files:
            logger.warning("No MKV files found in input directory")
        else:
            logger.info(f"Found {len(self.mkv_files)} MKV file(s)")

    def _check_already_converted(self, input_file: Path) -> bool:
        """Check if a file has already been converted.

        Args:
            input_file: Path to the input MKV file

        Returns:
            bool: True if output file exists
        """
        output_file: Path = self.converter._generate_output_path(input_file)
        return output_file.exists()

    def _display_file_list(self, show_details: bool = False) -> None:
        """Display list of MKV files with status.

        Args:
            show_details: Whether to show detailed video information
        """
        if not self.mkv_files:
            print("\n⚠️  No MKV files found.")
            print(f"   Place your MKV files in: {self.config.input_folder}")
            return

        # Calculate statistics
        total_files: int = len(self.mkv_files)
        total_size: int = sum(f.stat().st_size for f in self.mkv_files)
        already_converted: int = sum(
            1 for f in self.mkv_files if self._check_already_converted(f)
        )
        pending: int = total_files - already_converted

        print("\n" + "="*70)
        print("                    📋 MKV FILES OVERVIEW")
        print("="*70)
        print(f"\n📊 Summary:")
        print(f"   Total files:       {total_files}")
        print(f"   Already converted: {already_converted}")
        print(f"   Pending:           {pending}")
        print(f"   Total size:        {format_file_size(total_size)}")
        print(f"\n📁 Input folder:  {self.config.input_folder}")
        print(f"📁 Output folder: {self.config.output_folder}")
        print(f"🎬 Target:        {self.config.video.resolution}p MP4")

        print("\n" + "="*70)
        print("                    📄 FILE LIST")
        print("="*70)

        for idx, mkv_file in enumerate(self.mkv_files, 1):
            size_bytes: int = mkv_file.stat().st_size
            size_str: str = format_file_size(size_bytes)
            already_converted: bool = self._check_already_converted(mkv_file)
            status: str = "✅ Converted" if already_converted else "⏳ Pending"

            print(f"\n  [{idx}] {mkv_file.name}")
            print(f"      Path:   {mkv_file}")
            print(f"      Size:   {size_str}")
            print(f"      Status: {status}")

            # Show detailed info if requested
            if show_details and validate_ffprobe():
                video_info = get_video_info(mkv_file)
                if video_info:
                    print(f"      Video Details:")
                    if "codec_name" in video_info:
                        print(f"        - Codec: {video_info['codec_name']}")
                    if "width" in video_info and "height" in video_info:
                        print(f"        - Resolution: {video_info['width']}x{video_info['height']}")
                    if "duration" in video_info:
                        try:
                            duration_sec = float(video_info['duration'])
                            duration_min = int(duration_sec // 60)
                            duration_sec_remainder = int(duration_sec % 60)
                            print(f"        - Duration: {duration_min}m {duration_sec_remainder}s")
                        except (ValueError, TypeError):
                            # Duration is not a valid number (e.g., 'N/A')
                            print(f"        - Duration: {video_info['duration']}")

        print("\n" + "="*70 + "\n")

    def _process_single_file(self) -> None:
        """Process a single selected MKV file."""
        if not self.mkv_files:
            print("\n⚠️  No MKV files available to process.")
            return

        # Display file list
        print("\n📋 Select a file to process:\n")
        for idx, mkv_file in enumerate(self.mkv_files, 1):
            already_converted: bool = self._check_already_converted(mkv_file)
            status: str = "✅" if already_converted else "⏳"
            print(f"  [{idx}] {status} {mkv_file.name}")

        print(f"  [0] Cancel")

        # Get user selection
        try:
            choice: str = input("\nEnter file number: ").strip()
            file_idx: int = int(choice)

            if file_idx == 0:
                print("❌ Cancelled")
                return

            if file_idx < 1 or file_idx > len(self.mkv_files):
                print("❌ Invalid selection")
                return

            selected_file: Path = self.mkv_files[file_idx - 1]

            # Check if already converted
            if self.config.skip_existing and self._check_already_converted(selected_file):
                print(f"\n⚠️  File already converted: {selected_file.name}")
                overwrite: str = input("   Re-convert anyway? (yes/no) [no]: ").strip().lower()
                if overwrite not in ['yes', 'y']:
                    print("❌ Skipped")
                    return

            # Process the file
            print(f"\n🎬 Processing: {selected_file.name}")
            print("="*70)

            result: ConversionResult = self.converter.process_file(selected_file)
            self.conversion_history.append(result)

            # Display result
            self._display_conversion_result(result)

        except ValueError:
            print("❌ Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\n\n⚠️  Processing interrupted by user")
        except Exception as e:
            logger.exception(f"Error processing file: {e}")
            print(f"❌ Error: {e}")

    def _process_all_files(self) -> None:
        """Process all pending MKV files in batch."""
        if not self.mkv_files:
            print("\n⚠️  No MKV files available to process.")
            return

        # Filter pending files
        pending_files: list[Path] = [
            f for f in self.mkv_files
            if not (self.config.skip_existing and self._check_already_converted(f))
        ]

        if not pending_files:
            print("\n✅ All files have already been converted!")
            print("   Use 'View files' to see the list.")
            return

        # Confirm batch processing
        print(f"\n🎬 Ready to process {len(pending_files)} file(s)")
        print(f"   Target: {self.config.video.resolution}p MP4")
        print(f"   Quality: CRF {self.config.video.crf}, Preset: {self.config.video.preset}")

        if self.config.subtitles.enabled:
            lang_info: str = f" ({self.config.subtitles.language})" if self.config.subtitles.language else ""
            print(f"   Subtitles: Enabled{lang_info}")
        else:
            print(f"   Subtitles: Disabled")

        confirm: str = input(f"\nProceed with batch conversion? (yes/no) [yes]: ").strip().lower()
        if confirm not in ['', 'yes', 'y']:
            print("❌ Cancelled")
            return

        # Process all files
        print("\n" + "="*70)
        print("               🚀 BATCH CONVERSION STARTED")
        print("="*70)

        start_time: datetime = datetime.now()
        results: list[ConversionResult] = []

        for idx, mkv_file in enumerate(pending_files, 1):
            print(f"\n[{idx}/{len(pending_files)}] Processing: {mkv_file.name}")
            print("-"*70)

            try:
                result: ConversionResult = self.converter.process_file(mkv_file)
                results.append(result)
                self.conversion_history.append(result)

                if result.success:
                    print(f"✅ Success: {mkv_file.name}")
                else:
                    print(f"❌ Failed: {mkv_file.name}")
                    if result.error_message:
                        print(f"   Error: {result.error_message[:100]}")

            except KeyboardInterrupt:
                print("\n\n⚠️  Batch processing interrupted by user")
                print(f"   Processed {idx-1} of {len(pending_files)} files")
                break
            except Exception as e:
                logger.exception(f"Unexpected error processing {mkv_file.name}: {e}")
                print(f"❌ Unexpected error: {e}")

        # Display summary
        total_time: float = (datetime.now() - start_time).total_seconds()
        print("\n" + "="*70)
        self.converter.generate_summary(results)
        print(f"⏱️  Batch processing completed in {self._format_duration(total_time)}")
        print("="*70 + "\n")

    def _display_conversion_result(self, result: ConversionResult) -> None:
        """Display detailed conversion result.

        Args:
            result: ConversionResult object to display
        """
        print("\n" + "="*70)
        if result.success:
            print("                ✅ CONVERSION SUCCESSFUL")
        else:
            print("                ❌ CONVERSION FAILED")
        print("="*70)

        print(f"\n📄 File: {result.input_file.name}")
        print(f"📁 Output: {result.output_file}")

        if result.success:
            print(f"\n📊 Statistics:")
            print(f"   Original size:  {result.original_size_mb:.2f} MB")
            print(f"   Converted size: {result.converted_size_mb:.2f} MB")

            if result.original_size_mb > 0:
                reduction: float = ((result.original_size_mb - result.converted_size_mb) / result.original_size_mb) * 100
                print(f"   Size reduction: {reduction:.1f}%")

            print(f"   Duration:       {self._format_duration(result.duration_seconds)}")
        else:
            print(f"\n❌ Error:")
            print(f"   {result.error_message}")

        print("="*70 + "\n")

    def _view_conversion_history(self) -> None:
        """Display conversion history from current session."""
        if not self.conversion_history:
            print("\n⚠️  No conversions performed in this session yet.")
            return

        print("\n" + "="*70)
        print("              📜 CONVERSION HISTORY (Current Session)")
        print("="*70)

        total_files: int = len(self.conversion_history)
        successful: int = sum(1 for r in self.conversion_history if r.success)
        failed: int = total_files - successful

        print(f"\n📊 Session Summary:")
        print(f"   Total conversions: {total_files}")
        print(f"   ✅ Successful:     {successful}")
        print(f"   ❌ Failed:         {failed}")

        print("\n📋 Conversion Log:")
        print("="*70)

        for idx, result in enumerate(self.conversion_history, 1):
            status: str = "✅" if result.success else "❌"
            print(f"\n  [{idx}] {status} {result.input_file.name}")

            if result.success:
                print(f"      {result.original_size_mb:.1f}MB → {result.converted_size_mb:.1f}MB")
                print(f"      Duration: {self._format_duration(result.duration_seconds)}")
            else:
                print(f"      Error: {result.error_message[:80] if result.error_message else 'Unknown error'}")

        print("\n" + "="*70 + "\n")

    def _view_current_settings(self) -> None:
        """Display current processing settings."""
        print("\n" + "="*70)
        print("                  ⚙️  CURRENT SETTINGS")
        print("="*70)

        print(f"\n📁 Directories:")
        print(f"   Input:  {self.config.input_folder}")
        print(f"   Output: {self.config.output_folder}")
        print(f"   Logs:   {self.config.logs_folder}")

        print(f"\n🎬 Video Settings:")
        print(f"   Resolution: {self.config.video.resolution}p")
        print(f"   Codec:      {self.config.video.codec}")
        print(f"   Quality:    CRF {self.config.video.crf}")
        print(f"   Preset:     {self.config.video.preset}")

        print(f"\n🔊 Audio Settings:")
        print(f"   Codec:   {self.config.audio.codec}")
        print(f"   Bitrate: {self.config.audio.bitrate}")

        print(f"\n📝 Subtitle Settings:")
        print(f"   Enabled:  {self.config.subtitles.enabled}")
        if self.config.subtitles.language:
            print(f"   Language: {self.config.subtitles.language}")

        print(f"\n⚙️  Processing Options:")
        print(f"   Skip existing:      {self.config.skip_existing}")
        print(f"   Parallel:           {self.config.parallel_processing}")
        if self.config.parallel_processing:
            print(f"   Max workers:        {self.config.max_workers}")
        print(f"   Verbose logging:    {self.config.verbose}")

        print("\n💡 To change settings, run: python scripts/config_manager.py")
        print("="*70 + "\n")

    def _show_welcome(self) -> None:
        """Display welcome message and system information."""
        print("\n" + "="*70)
        print("                 🎬 MKV to MP4 Batch Processor")
        print("                   Step 4: Process Each File")
        print("="*70)

        # Check FFmpeg
        if not validate_ffmpeg():
            print("\n⚠️  WARNING: FFmpeg not found in system PATH!")
            print("   Please install FFmpeg before processing files.")
            print("\n   Installation:")
            print("     macOS:   brew install ffmpeg")
            print("     Ubuntu:  sudo apt install ffmpeg")
            print("     Windows: choco install ffmpeg")
            print("\n" + "="*70)
            return

        print("\n✅ FFmpeg is installed and ready")

        # Scan for files
        self._scan_files()

        if self.mkv_files:
            pending: int = sum(
                1 for f in self.mkv_files
                if not self._check_already_converted(f)
            )
            print(f"📁 Found {len(self.mkv_files)} MKV file(s)")
            print(f"⏳ {pending} file(s) pending conversion")
        else:
            print(f"📁 No MKV files found in: {self.config.input_folder}")

        print("="*70)

    def _show_help(self) -> None:
        """Display help information."""
        print("\n" + "="*70)
        print("                        📚 HELP & TIPS")
        print("="*70)

        print("\n🎯 WHAT THIS TOOL DOES:")
        print("   This script processes MKV files and converts them to MP4 format")
        print("   with hard-coded subtitles using FFmpeg. You can:")
        print("   • View all MKV files and their conversion status")
        print("   • Process individual files")
        print("   • Batch process all pending files")
        print("   • View conversion results and statistics")

        print("\n📋 WORKFLOW:")
        print("   1. Place MKV files in the input folder")
        print("   2. Use 'View files' to see what's available")
        print("   3. Choose 'Process all' for batch conversion or")
        print("      'Process single file' to convert one at a time")
        print("   4. Converted MP4 files will be in the output folder")

        print("\n⚙️  SETTINGS:")
        print("   Current settings are loaded from config.yaml")
        print("   To change settings, run: python scripts/config_manager.py")
        print("   Settings include resolution, quality, codecs, etc.")

        print("\n💡 TIPS:")
        print("   • Processing time depends on file size and quality settings")
        print("   • Lower CRF = better quality but larger files")
        print("   • Skip existing files to avoid re-converting")
        print("   • Check logs/ folder for detailed conversion logs")
        print("   • Press Ctrl+C to interrupt long-running conversions")

        print("\n📁 FILE LOCATIONS:")
        print(f"   Config:  {self.config_path.absolute()}")
        print(f"   Input:   {self.config.input_folder.absolute()}")
        print(f"   Output:  {self.config.output_folder.absolute()}")
        print(f"   Logs:    {self.config.logs_folder.absolute()}")

        print("="*70)
        input("\nPress Enter to continue...")

    @staticmethod
    def _format_duration(seconds: float) -> str:
        """Format duration in human-readable format.

        Args:
            seconds: Duration in seconds

        Returns:
            str: Formatted duration string

        Example:
            >>> MKVProcessor._format_duration(3725)
            '1h 2m 5s'
        """
        mins, secs = divmod(int(seconds), 60)
        hours, mins = divmod(mins, 60)

        if hours > 0:
            return f"{hours}h {mins}m {secs}s"
        elif mins > 0:
            return f"{mins}m {secs}s"
        else:
            return f"{secs}s"

    def run(self) -> None:
        """Run the interactive MKV processor."""
        self._show_welcome()

        while True:
            print("\n📋 Main Menu:")
            print("  1. View files and status")
            print("  2. View files with details (requires ffprobe)")
            print("  3. Process single file")
            print("  4. Process all pending files")
            print("  5. View conversion history (current session)")
            print("  6. View current settings")
            print("  7. Refresh file list")
            print("  H. Show help")
            print("  0. Exit")

            choice: str = input("\nSelect option: ").strip().lower()

            if choice == "1":
                self._display_file_list(show_details=False)
            elif choice == "2":
                if not validate_ffprobe():
                    print("\n⚠️  ffprobe not found. Install FFmpeg to enable this feature.")
                else:
                    self._display_file_list(show_details=True)
            elif choice == "3":
                self._process_single_file()
            elif choice == "4":
                self._process_all_files()
            elif choice == "5":
                self._view_conversion_history()
            elif choice == "6":
                self._view_current_settings()
            elif choice == "7":
                print("\n🔄 Refreshing file list...")
                self._scan_files()
                print(f"✓ Found {len(self.mkv_files)} MKV file(s)")
            elif choice == "h":
                self._show_help()
            elif choice == "0":
                print("\n👋 Goodbye!")
                print("   Check your output folder for converted files.")
                break
            else:
                print("❌ Invalid option. Please try again.")


def main() -> int:
    """Main entry point for MKV processor script.

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Interactive MKV to MP4 batch processor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default config
  python scripts/process_mkv_files.py

  # Run with custom config
  python scripts/process_mkv_files.py --config my_config.yaml
        """
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)"
    )
    args = parser.parse_args()

    try:
        # Create and run processor
        processor = MKVProcessor(config_path=args.config)
        processor.run()
        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        return 130
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        print(f"\n❌ Fatal error: {e}")
        print("   Check logs for details")
        return 1


if __name__ == "__main__":
    sys.exit(main())
