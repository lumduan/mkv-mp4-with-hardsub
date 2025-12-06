#!/usr/bin/env python3
"""Interactive CLI tool for managing config.yaml settings.

This script provides a user-friendly menu-driven interface for:
- Quick setup wizard for first-time users
- Viewing current configuration
- Updating settings interactively
- Validating configuration
- Resetting to defaults

Usage:
    python scripts/config_manager.py
    # or
    chmod +x scripts/config_manager.py
    ./scripts/config_manager.py
"""

import sys
from pathlib import Path
from typing import Optional

# Add parent directory to path to import src modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Check Python version and warn about unstable versions
if sys.version_info >= (3, 14) and "a" in sys.version.lower():
    print("\n⚠️  WARNING: You are using Python 3.14 alpha version!")
    print("   This may cause crashes with some dependencies (pydantic).")
    print("   Recommended: Use Python 3.10, 3.11, 3.12, or 3.13 stable release.\n")
    response = input("Continue anyway? (yes/no) [no]: ").strip().lower()
    if response not in ['yes', 'y']:
        print("Exiting. Please use a stable Python version.")
        sys.exit(1)

try:
    from src.config import load_config, save_config, Config, VideoConfig, AudioConfig, SubtitleConfig
except Exception as e:
    print(f"\n❌ Error loading configuration modules: {e}")
    print("\nPossible solutions:")
    print("  1. Install dependencies: uv sync")
    print("  2. Use a stable Python version (3.10-3.13)")
    print("  3. Check if pydantic is installed correctly")
    sys.exit(1)


class ConfigManager:
    """Interactive configuration manager."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize the config manager.

        Args:
            config_path: Path to the configuration file
        """
        self.config_path = Path(config_path)
        self.config: Optional[Config] = None
        self.is_first_run = not self.config_path.exists()
        self.load_configuration()

    def load_configuration(self) -> None:
        """Load the current configuration."""
        try:
            self.config = load_config(self.config_path)
            print(f"✓ Configuration loaded from {self.config_path}")
        except Exception as e:
            print(f"✗ Error loading configuration: {e}")
            print("  Using default configuration")
            self.config = Config()

    def save_configuration(self) -> None:
        """Save the current configuration."""
        try:
            save_config(self.config, self.config_path)
            print(f"✓ Configuration saved to {self.config_path}")
        except Exception as e:
            print(f"✗ Error saving configuration: {e}")

    def display_config(self) -> None:
        """Display current configuration."""
        print("\n" + "=" * 60)
        print("CURRENT CONFIGURATION")
        print("=" * 60)
        print(f"\n📁 Directory Settings:")
        print(f"   Input Folder:    {self.config.input_folder}")
        print(f"   Output Folder:   {self.config.output_folder}")
        print(f"   Logs Folder:     {self.config.logs_folder}")

        print(f"\n🎬 Video Settings:")
        print(f"   Resolution:      {self.config.video.resolution}p")
        print(f"   Codec:           {self.config.video.codec}")
        print(f"   CRF (Quality):   {self.config.video.crf}")
        print(f"   Preset:          {self.config.video.preset}")

        print(f"\n🔊 Audio Settings:")
        print(f"   Codec:           {self.config.audio.codec}")
        print(f"   Bitrate:         {self.config.audio.bitrate}")

        print(f"\n📝 Subtitle Settings:")
        print(f"   Enabled:         {self.config.subtitles.enabled}")
        print(f"   Language:        {self.config.subtitles.language or 'Default'}")
        print(f"   Force Style:     {self.config.subtitles.force_style or 'None'}")

        print(f"\n⚙️  Processing Options:")
        print(f"   Parallel:        {self.config.parallel_processing}")
        print(f"   Max Workers:     {self.config.max_workers}")
        print(f"   Skip Existing:   {self.config.skip_existing}")
        print(f"   Verbose:         {self.config.verbose}")
        print("=" * 60 + "\n")

    def update_directories(self) -> None:
        """Update directory settings."""
        print("\n📁 Directory Settings")
        print("-" * 40)

        input_folder = input(f"Input folder [{self.config.input_folder}]: ").strip()
        if input_folder:
            self.config.input_folder = Path(input_folder)

        output_folder = input(f"Output folder [{self.config.output_folder}]: ").strip()
        if output_folder:
            self.config.output_folder = Path(output_folder)

        logs_folder = input(f"Logs folder [{self.config.logs_folder}]: ").strip()
        if logs_folder:
            self.config.logs_folder = Path(logs_folder)

        print("✓ Directory settings updated")

    def update_video_settings(self) -> None:
        """Update video encoding settings."""
        print("\n🎬 Video Encoding Settings")
        print("-" * 40)

        resolution = input(f"Resolution (144-2160) [{self.config.video.resolution}]: ").strip()
        if resolution:
            try:
                self.config.video.resolution = int(resolution)
            except ValueError:
                print("✗ Invalid resolution. Keeping current value.")

        print("\nAvailable codecs: libx264, libx265, h264, hevc")
        codec = input(f"Video codec [{self.config.video.codec}]: ").strip()
        if codec:
            try:
                # Trigger validation by creating new VideoConfig
                test_config = VideoConfig(
                    resolution=self.config.video.resolution,
                    codec=codec,
                    crf=self.config.video.crf,
                    preset=self.config.video.preset
                )
                self.config.video.codec = codec
            except ValueError as e:
                print(f"✗ {e}")

        crf = input(f"CRF quality (0-51, lower=better) [{self.config.video.crf}]: ").strip()
        if crf:
            try:
                crf_val = int(crf)
                if 0 <= crf_val <= 51:
                    self.config.video.crf = crf_val
                else:
                    print("✗ CRF must be between 0 and 51. Keeping current value.")
            except ValueError:
                print("✗ Invalid CRF. Keeping current value.")

        print("\nAvailable presets: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow")
        preset = input(f"Encoding preset [{self.config.video.preset}]: ").strip()
        if preset:
            try:
                test_config = VideoConfig(
                    resolution=self.config.video.resolution,
                    codec=self.config.video.codec,
                    crf=self.config.video.crf,
                    preset=preset
                )
                self.config.video.preset = preset
            except ValueError as e:
                print(f"✗ {e}")

        print("✓ Video settings updated")

    def update_audio_settings(self) -> None:
        """Update audio encoding settings."""
        print("\n🔊 Audio Encoding Settings")
        print("-" * 40)

        print("Available codecs: aac, mp3, opus, ac3")
        codec = input(f"Audio codec [{self.config.audio.codec}]: ").strip()
        if codec:
            try:
                test_config = AudioConfig(codec=codec, bitrate=self.config.audio.bitrate)
                self.config.audio.codec = codec
            except ValueError as e:
                print(f"✗ {e}")

        bitrate = input(f"Audio bitrate (e.g., 128k, 192k) [{self.config.audio.bitrate}]: ").strip()
        if bitrate:
            try:
                test_config = AudioConfig(codec=self.config.audio.codec, bitrate=bitrate)
                self.config.audio.bitrate = bitrate
            except ValueError as e:
                print(f"✗ {e}")

        print("✓ Audio settings updated")

    def update_subtitle_settings(self) -> None:
        """Update subtitle settings."""
        print("\n📝 Subtitle Settings")
        print("-" * 40)

        enabled = input(f"Enable subtitles? (yes/no) [{('yes' if self.config.subtitles.enabled else 'no')}]: ").strip().lower()
        if enabled in ['yes', 'y']:
            self.config.subtitles.enabled = True
        elif enabled in ['no', 'n']:
            self.config.subtitles.enabled = False

        language = input(f"Subtitle language code (or blank for default) [{self.config.subtitles.language or ''}]: ").strip()
        self.config.subtitles.language = language if language else None

        force_style = input(f"Custom subtitle style (or blank) [{self.config.subtitles.force_style or ''}]: ").strip()
        self.config.subtitles.force_style = force_style if force_style else None

        print("✓ Subtitle settings updated")

    def update_processing_options(self) -> None:
        """Update processing options."""
        print("\n⚙️  Processing Options")
        print("-" * 40)

        parallel = input(f"Enable parallel processing? (yes/no) [{('yes' if self.config.parallel_processing else 'no')}]: ").strip().lower()
        if parallel in ['yes', 'y']:
            self.config.parallel_processing = True
        elif parallel in ['no', 'n']:
            self.config.parallel_processing = False

        workers = input(f"Max workers (1-16) [{self.config.max_workers}]: ").strip()
        if workers:
            try:
                workers_val = int(workers)
                if 1 <= workers_val <= 16:
                    self.config.max_workers = workers_val
                else:
                    print("✗ Max workers must be between 1 and 16. Keeping current value.")
            except ValueError:
                print("✗ Invalid value. Keeping current value.")

        skip = input(f"Skip existing files? (yes/no) [{('yes' if self.config.skip_existing else 'no')}]: ").strip().lower()
        if skip in ['yes', 'y']:
            self.config.skip_existing = True
        elif skip in ['no', 'n']:
            self.config.skip_existing = False

        verbose = input(f"Enable verbose logging? (yes/no) [{('yes' if self.config.verbose else 'no')}]: ").strip().lower()
        if verbose in ['yes', 'y']:
            self.config.verbose = True
        elif verbose in ['no', 'n']:
            self.config.verbose = False

        print("✓ Processing options updated")

    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults."""
        confirm = input("\n⚠️  Are you sure you want to reset to default configuration? (yes/no): ").strip().lower()
        if confirm in ['yes', 'y']:
            self.config = Config()
            print("✓ Configuration reset to defaults")
        else:
            print("✗ Reset cancelled")

    def show_welcome(self) -> None:
        """Display welcome message and configuration guide."""
        print("\n" + "=" * 70)
        print(" " * 15 + "🎬 MKV to MP4 Converter")
        print(" " * 15 + "Configuration Manager")
        print("=" * 70)
        print("\n📝 About config.yaml:")
        print("   The config.yaml file controls how your videos are converted.")
        print("   You can customize:")
        print("   • Video quality (resolution, codec, quality level)")
        print("   • Audio settings (codec, bitrate)")
        print("   • Subtitle preferences (language, styling)")
        print("   • Processing options (parallel processing, etc.)")
        print("\n💡 Tips:")
        print("   • Lower CRF value = Better quality but larger file size")
        print("   • Higher resolution = Better quality but slower conversion")
        print("   • Enable parallel processing if you have a multi-core CPU")
        print("=" * 70)

    def show_help(self) -> None:
        """Display detailed help information."""
        print("\n" + "=" * 70)
        print("📚 Configuration Help & Tips")
        print("=" * 70)

        print("\n🎬 VIDEO SETTINGS:")
        print("   Resolution:")
        print("     • 480p  - Smaller files, faster encoding (SD quality)")
        print("     • 720p  - Good balance of quality and file size (HD)")
        print("     • 1080p - High quality, larger files (Full HD)")

        print("\n   CRF (Constant Rate Factor):")
        print("     • 18-20 - Very high quality (large files)")
        print("     • 23-24 - Good quality (recommended)")
        print("     • 28-30 - Lower quality (smaller files)")

        print("\n   Codec:")
        print("     • libx264 - H.264 codec, best compatibility")
        print("     • libx265 - H.265/HEVC, better compression but slower")

        print("\n   Preset:")
        print("     • fast/faster   - Quick encoding, larger files")
        print("     • medium        - Balanced (recommended)")
        print("     • slow/slower   - Better compression, takes longer")

        print("\n🔊 AUDIO SETTINGS:")
        print("   • AAC (128k-192k) - Best compatibility and quality")
        print("   • MP3 (128k-320k) - Universal compatibility")

        print("\n📝 SUBTITLE SETTINGS:")
        print("   • Enabled: Subtitles are burned into the video permanently")
        print("   • Language: Use 3-letter codes (eng, tha, jpn, chi, etc.)")
        print("   • Leave blank to use default subtitle track")

        print("\n⚙️  PROCESSING OPTIONS:")
        print("   • Parallel Processing: Process multiple files at once")
        print("     WARNING: Uses more CPU and RAM")
        print("   • Max Workers: How many files to process simultaneously")
        print("     Recommended: Number of CPU cores - 1")
        print("   • Skip Existing: Don't re-convert files that already exist")

        print("\n💡 COMMON PRESETS:")
        print("   Small Files, Fast:  480p, CRF 28, preset fast")
        print("   Balanced Quality:   480p, CRF 24, preset medium")
        print("   High Quality:       720p, CRF 20, preset slow")
        print("   Archive Quality:    1080p, CRF 18, preset slower")

        print("\n📍 FILE LOCATIONS:")
        print(f"   Config file:   {self.config_path.absolute()}")
        print(f"   Input folder:  {self.config.input_folder}")
        print(f"   Output folder: {self.config.output_folder}")
        print(f"   Logs folder:   {self.config.logs_folder}")

        print("=" * 70)
        input("\n Press Enter to continue...")

    def quick_setup_wizard(self) -> None:
        """Run quick setup wizard for first-time users."""
        print("\n" + "=" * 70)
        print("🚀 Quick Setup Wizard")
        print("=" * 70)
        print("\nLet's configure your video converter with a few simple questions.\n")

        # Quality preset
        print("📊 Choose quality preset:")
        print("  1. High Quality (720p, CRF 20) - Larger files, better quality")
        print("  2. Balanced (480p, CRF 24) - Recommended for most users")
        print("  3. Smaller Files (480p, CRF 28) - Faster conversion, smaller files")

        quality = input("\nSelect preset (1-3) [2]: ").strip() or "2"

        if quality == "1":
            self.config.video.resolution = 720
            self.config.video.crf = 20
            print("✓ High quality preset selected")
        elif quality == "3":
            self.config.video.resolution = 480
            self.config.video.crf = 28
            print("✓ Smaller files preset selected")
        else:
            self.config.video.resolution = 480
            self.config.video.crf = 24
            print("✓ Balanced preset selected")

        # Subtitle settings
        print("\n📝 Subtitle settings:")
        subtitles = input("Do you want to burn subtitles into the video? (yes/no) [yes]: ").strip().lower() or "yes"
        self.config.subtitles.enabled = subtitles in ['yes', 'y']

        if self.config.subtitles.enabled:
            lang = input("Preferred subtitle language code (e.g., eng, tha, jpn) [auto]: ").strip()
            if lang and lang.lower() != "auto":
                self.config.subtitles.language = lang
                print(f"✓ Will use '{lang}' subtitles when available")
            else:
                print("✓ Will use default subtitle track")
        else:
            print("✓ Subtitles disabled")

        # Parallel processing
        print("\n⚙️  Performance settings:")
        parallel = input("Enable parallel processing for faster conversion? (yes/no) [no]: ").strip().lower() or "no"
        self.config.parallel_processing = parallel in ['yes', 'y']

        if self.config.parallel_processing:
            workers = input("How many files to process simultaneously? (1-4) [2]: ").strip() or "2"
            try:
                self.config.max_workers = min(4, max(1, int(workers)))
                print(f"✓ Will process {self.config.max_workers} files in parallel")
            except ValueError:
                print("✓ Using default: 2 workers")

        # Directories
        print("\n📁 Directory settings:")
        print("   Input folder:  Where your MKV files are located")
        print("   Output folder: Where converted MP4 files will be saved")

        change_dirs = input("\nUse default folders (input/, output/)? (yes/no) [yes]: ").strip().lower() or "yes"
        if change_dirs not in ['yes', 'y']:
            input_dir = input("Input folder path: ").strip()
            if input_dir:
                self.config.input_folder = Path(input_dir)

            output_dir = input("Output folder path: ").strip()
            if output_dir:
                self.config.output_folder = Path(output_dir)

        print("\n" + "=" * 70)
        print("✨ Setup complete! Your configuration:")
        print("=" * 70)
        self.display_config()

        save = input("\n💾 Save this configuration to config.yaml? (yes/no) [yes]: ").strip().lower() or "yes"
        if save in ['yes', 'y']:
            self.save_configuration()
            print("\n✅ Configuration saved! You can now run the converter.")
            print("   To make changes later, run this script again.")
        else:
            print("\n⚠️  Configuration not saved. Run setup again to configure.")

    def run(self) -> None:
        """Run the interactive configuration manager."""
        self.show_welcome()

        # If first run, offer quick setup
        if self.is_first_run:
            print("\n🎯 It looks like this is your first time setting up.")
            run_wizard = input("Would you like to run the Quick Setup Wizard? (yes/no) [yes]: ").strip().lower() or "yes"
            if run_wizard in ['yes', 'y']:
                self.quick_setup_wizard()
                return

        while True:
            print("\n📋 Main Menu:")
            print("  1. View current configuration")
            print("  2. 🚀 Quick Setup Wizard (Easy configuration)")
            print("  3. Update directory settings")
            print("  4. Update video settings")
            print("  5. Update audio settings")
            print("  6. Update subtitle settings")
            print("  7. Update processing options")
            print("  8. Save configuration")
            print("  9. Reset to defaults")
            print("  R. Reload configuration from file")
            print("  H. Show help and tips")
            print("  0. Exit")

            choice = input("\nSelect option: ").strip().lower()

            if choice == "1":
                self.display_config()
            elif choice == "2":
                self.quick_setup_wizard()
            elif choice == "3":
                self.update_directories()
            elif choice == "4":
                self.update_video_settings()
            elif choice == "5":
                self.update_audio_settings()
            elif choice == "6":
                self.update_subtitle_settings()
            elif choice == "7":
                self.update_processing_options()
            elif choice == "8":
                self.save_configuration()
            elif choice == "9":
                self.reset_to_defaults()
            elif choice == "r":
                self.load_configuration()
            elif choice == "h":
                self.show_help()
            elif choice == "0":
                print("\n👋 Goodbye!")
                break
            else:
                print("✗ Invalid option. Please try again.")


def main() -> None:
    """Main entry point."""
    config_path = "config.yaml"

    # Check if custom config path provided
    if len(sys.argv) > 1:
        config_path = sys.argv[1]

    manager = ConfigManager(config_path)
    manager.run()


if __name__ == "__main__":
    main()
