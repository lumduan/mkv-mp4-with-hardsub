#!/usr/bin/env python3
"""Interactive CLI tool for managing config.yaml settings.

This script provides a user-friendly menu-driven interface for:
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

# Add parent directory to path to import src modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import load_config, save_config, Config, VideoConfig, AudioConfig, SubtitleConfig
from typing import Optional


class ConfigManager:
    """Interactive configuration manager."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize the config manager.

        Args:
            config_path: Path to the configuration file
        """
        self.config_path = Path(config_path)
        self.config: Optional[Config] = None
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

    def run(self) -> None:
        """Run the interactive configuration manager."""
        print("\n" + "=" * 60)
        print("MKV to MP4 Converter - Configuration Manager")
        print("=" * 60)

        while True:
            print("\n📋 Main Menu:")
            print("  1. View current configuration")
            print("  2. Update directory settings")
            print("  3. Update video settings")
            print("  4. Update audio settings")
            print("  5. Update subtitle settings")
            print("  6. Update processing options")
            print("  7. Save configuration")
            print("  8. Reset to defaults")
            print("  9. Reload configuration")
            print("  0. Exit")

            choice = input("\nSelect option (0-9): ").strip()

            if choice == "1":
                self.display_config()
            elif choice == "2":
                self.update_directories()
            elif choice == "3":
                self.update_video_settings()
            elif choice == "4":
                self.update_audio_settings()
            elif choice == "5":
                self.update_subtitle_settings()
            elif choice == "6":
                self.update_processing_options()
            elif choice == "7":
                self.save_configuration()
            elif choice == "8":
                self.reset_to_defaults()
            elif choice == "9":
                self.load_configuration()
            elif choice == "0":
                print("\n👋 Goodbye!")
                break
            else:
                print("✗ Invalid option. Please select 0-9.")


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
