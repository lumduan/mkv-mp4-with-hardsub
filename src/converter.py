"""Core conversion logic for batch MKV to MP4 conversion."""

from pathlib import Path
from typing import Any
import subprocess
from dataclasses import dataclass
from datetime import datetime
from loguru import logger

from src.config import Config


@dataclass
class ConversionResult:
    """Result of a single file conversion.

    Attributes:
        input_file: Path to the input MKV file
        output_file: Path to the output MP4 file
        success: Whether the conversion was successful
        duration_seconds: Time taken for conversion in seconds
        original_size_mb: Size of original file in megabytes
        converted_size_mb: Size of converted file in megabytes
        error_message: Error message if conversion failed
    """

    input_file: Path
    output_file: Path
    success: bool
    duration_seconds: float
    original_size_mb: float
    converted_size_mb: float
    error_message: str | None = None


class BatchConverter:
    """Batch MKV to MP4 converter with hard-sub.

    This class handles the batch conversion of MKV files to MP4 format
    with hard-coded subtitles using FFmpeg.

    Attributes:
        config: Configuration object containing all settings
    """

    def __init__(self, config: Config) -> None:
        """Initialize batch converter.

        Args:
            config: Configuration object with conversion settings
        """
        self.config: Config = config
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Create output and logs directories if they don't exist."""
        self.config.output_folder.mkdir(parents=True, exist_ok=True)
        self.config.logs_folder.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured directories exist: output={self.config.output_folder}, logs={self.config.logs_folder}")

    def scan_input_folder(self) -> list[Path]:
        """Scan input folder for MKV files.

        Recursively searches the input directory for .mkv files,
        filtering out hidden files and system files.

        Returns:
            list[Path]: Sorted list of MKV file paths found

        Examples:
            >>> converter = BatchConverter(config)
            >>> mkv_files = converter.scan_input_folder()
            >>> print(f"Found {len(mkv_files)} MKV files")
        """
        input_path: Path = self.config.input_folder

        if not input_path.exists():
            logger.error(f"Input folder not found: {input_path}")
            return []

        if not input_path.is_dir():
            logger.error(f"Input path is not a directory: {input_path}")
            return []

        # Recursively find all .mkv files
        all_mkv_files: list[Path] = list(input_path.glob("**/*.mkv"))

        # Filter out hidden files (files/directories starting with .)
        mkv_files: list[Path] = [
            f for f in all_mkv_files
            if not any(part.startswith('.') for part in f.parts)
        ]

        # Sort alphabetically for consistent processing
        mkv_files = sorted(mkv_files)

        logger.info(f"Found {len(mkv_files)} MKV file(s) in {input_path}")
        if mkv_files:
            logger.debug(f"Files to process: {[f.name for f in mkv_files]}")

        return mkv_files

    def _generate_output_path(self, input_file: Path) -> Path:
        """Generate output filename with _480p suffix.

        Args:
            input_file: Path to the input MKV file

        Returns:
            Path: Path for the output MP4 file

        Examples:
            >>> input_file = Path("input/movies/avatar.mkv")
            >>> output = converter._generate_output_path(input_file)
            >>> print(output)
            Path("output/movies/avatar_480p.mp4")
        """
        relative_path: Path = input_file.relative_to(self.config.input_folder)
        output_name: str = f"{input_file.stem}_{self.config.video.resolution}p.mp4"
        output_path: Path = self.config.output_folder / relative_path.parent / output_name

        # Create subdirectories if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)

        return output_path

    def _build_ffmpeg_command(self, input_file: Path, output_file: Path) -> list[str]:
        """Construct FFmpeg command for conversion.

        Args:
            input_file: Path to the input MKV file
            output_file: Path to the output MP4 file

        Returns:
            list[str]: FFmpeg command as list of arguments
        """
        cmd: list[str] = [
            "ffmpeg",
            "-i", str(input_file),
        ]

        # Add subtitle filter if enabled
        if self.config.subtitles.enabled:
            # Build subtitle filter
            subtitle_filter = f"subtitles={input_file}"

            # Add language specification if provided
            if self.config.subtitles.language:
                subtitle_filter += f":si={self.config.subtitles.language}"

            # Add custom style if provided
            if self.config.subtitles.force_style:
                subtitle_filter += f":force_style='{self.config.subtitles.force_style}'"

            # Combine with scale filter
            vf_filter = f"{subtitle_filter},scale=-2:{self.config.video.resolution}"
        else:
            vf_filter = f"scale=-2:{self.config.video.resolution}"

        cmd.extend([
            "-vf", vf_filter,
            "-vcodec", self.config.video.codec,
            "-acodec", self.config.audio.codec,
            "-crf", str(self.config.video.crf),
            "-preset", self.config.video.preset,
            "-b:a", self.config.audio.bitrate,
            "-movflags", "+faststart",
            "-y",  # Overwrite output file if exists
            str(output_file)
        ])

        return cmd

    def process_file(self, input_file: Path) -> ConversionResult:
        """Process a single MKV file.

        Args:
            input_file: Path to the MKV file to convert

        Returns:
            ConversionResult: Object containing conversion results and metadata
        """
        start_time: datetime = datetime.now()
        output_file: Path = self._generate_output_path(input_file)

        # Skip if output already exists and skip_existing is True
        if self.config.skip_existing and output_file.exists():
            logger.info(f"Skipping {input_file.name} (already converted)")
            return ConversionResult(
                input_file=input_file,
                output_file=output_file,
                success=True,
                duration_seconds=0,
                original_size_mb=0,
                converted_size_mb=output_file.stat().st_size / (1024 * 1024),
            )

        try:
            # Get original file size
            original_size_mb: float = input_file.stat().st_size / (1024 * 1024)

            # Build FFmpeg command
            cmd: list[str] = self._build_ffmpeg_command(input_file, output_file)

            logger.info(f"Converting: {input_file.name}")
            if self.config.verbose:
                logger.debug(f"FFmpeg command: {' '.join(cmd)}")

            # Execute FFmpeg
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

            # Calculate duration
            duration: float = (datetime.now() - start_time).total_seconds()

            # Validate output
            if not output_file.exists() or output_file.stat().st_size == 0:
                raise ValueError("Output file is missing or empty")

            converted_size_mb: float = output_file.stat().st_size / (1024 * 1024)

            # Log success with extra context
            logger.success(
                f"{input_file.name} → {output_file.name} | "
                f"{original_size_mb:.1f}MB → {converted_size_mb:.1f}MB | "
                f"{duration:.1f}s"
            )

            return ConversionResult(
                input_file=input_file,
                output_file=output_file,
                success=True,
                duration_seconds=duration,
                original_size_mb=original_size_mb,
                converted_size_mb=converted_size_mb,
            )

        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg error for {input_file.name}: {e.stderr}")
            return ConversionResult(
                input_file=input_file,
                output_file=output_file,
                success=False,
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                original_size_mb=input_file.stat().st_size / (1024 * 1024),
                converted_size_mb=0,
                error_message=str(e.stderr)
            )
        except Exception as e:
            logger.exception(f"Unexpected error for {input_file.name}")
            return ConversionResult(
                input_file=input_file,
                output_file=output_file,
                success=False,
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                original_size_mb=input_file.stat().st_size / (1024 * 1024),
                converted_size_mb=0,
                error_message=str(e)
            )

    def process_all(self, mkv_files: list[Path]) -> list[ConversionResult]:
        """Process all MKV files.

        Args:
            mkv_files: List of MKV file paths to process

        Returns:
            list[ConversionResult]: List of conversion results
        """
        results: list[ConversionResult] = []

        for mkv_file in mkv_files:
            result: ConversionResult = self.process_file(mkv_file)
            results.append(result)

        return results

    def generate_summary(self, results: list[ConversionResult]) -> None:
        """Generate and display summary report.

        Args:
            results: List of conversion results to summarize
        """
        total_files: int = len(results)
        successful: int = sum(1 for r in results if r.success)
        failed: int = total_files - successful

        total_original_size: float = sum(r.original_size_mb for r in results)
        total_converted_size: float = sum(r.converted_size_mb for r in results)
        space_saved: float = total_original_size - total_converted_size
        space_saved_percent: float = (space_saved / total_original_size * 100) if total_original_size > 0 else 0

        total_time: float = sum(r.duration_seconds for r in results)

        # Print summary
        print("\n" + "="*50)
        print("     CONVERSION SUMMARY REPORT")
        print("="*50)
        print(f"\nTotal Files Processed:  {total_files}")
        print(f"✅ Successful:          {successful}")
        print(f"❌ Failed:              {failed}")
        print(f"⏱️  Total Time:         {self._format_duration(total_time)}")
        print(f"\nOriginal Total Size:    {total_original_size:.2f} MB")
        print(f"Converted Total Size:   {total_converted_size:.2f} MB")
        print(f"Space Saved:            {space_saved:.2f} MB ({space_saved_percent:.1f}%)")

        if failed > 0:
            print("\nFailed Files:")
            for i, result in enumerate([r for r in results if not r.success], 1):
                print(f"  {i}. {result.input_file.name} - {result.error_message}")

        print("="*50 + "\n")

    @staticmethod
    def _format_duration(seconds: float) -> str:
        """Format duration in human-readable format.

        Args:
            seconds: Duration in seconds

        Returns:
            str: Formatted duration string (e.g., "2h 15m 30s")
        """
        mins, secs = divmod(int(seconds), 60)
        hours, mins = divmod(mins, 60)

        if hours > 0:
            return f"{hours}h {mins}m {secs}s"
        elif mins > 0:
            return f"{mins}m {secs}s"
        else:
            return f"{secs}s"
