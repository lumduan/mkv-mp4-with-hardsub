"""Configuration management with validation."""

from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml


class VideoConfig(BaseModel):
    """Video encoding settings.

    Attributes:
        resolution: Target height in pixels (e.g., 480 for 480p)
        codec: Video codec to use (libx264, libx265, etc.)
        crf: Constant Rate Factor (0-51, lower = better quality)
        preset: Encoding speed preset (ultrafast to veryslow)
    """

    resolution: int = Field(
        default=480,
        description="Target height in pixels",
        ge=144,
        le=2160
    )
    codec: str = Field(
        default="libx264",
        description="Video codec"
    )
    crf: int = Field(
        default=24,
        ge=0,
        le=51,
        description="Constant Rate Factor (quality)"
    )
    preset: str = Field(
        default="medium",
        description="Encoding preset"
    )

    @field_validator("preset")
    @classmethod
    def validate_preset(cls, v: str) -> str:
        """Validate FFmpeg preset.

        Args:
            v: Preset value to validate

        Returns:
            Validated preset value

        Raises:
            ValueError: If preset is not valid
        """
        valid_presets = [
            "ultrafast", "superfast", "veryfast", "faster",
            "fast", "medium", "slow", "slower", "veryslow"
        ]
        if v not in valid_presets:
            raise ValueError(
                f"Invalid preset '{v}'. Choose from: {', '.join(valid_presets)}"
            )
        return v

    @field_validator("codec")
    @classmethod
    def validate_codec(cls, v: str) -> str:
        """Validate video codec.

        Args:
            v: Codec value to validate

        Returns:
            Validated codec value

        Raises:
            ValueError: If codec is not supported
        """
        valid_codecs = ["libx264", "libx265", "h264", "hevc"]
        if v not in valid_codecs:
            raise ValueError(
                f"Invalid codec '{v}'. Choose from: {', '.join(valid_codecs)}"
            )
        return v


class AudioConfig(BaseModel):
    """Audio encoding settings.

    Attributes:
        codec: Audio codec to use
        bitrate: Audio bitrate (e.g., '128k', '192k')
    """

    codec: str = Field(
        default="aac",
        description="Audio codec"
    )
    bitrate: str = Field(
        default="128k",
        description="Audio bitrate"
    )

    @field_validator("codec")
    @classmethod
    def validate_codec(cls, v: str) -> str:
        """Validate audio codec.

        Args:
            v: Codec value to validate

        Returns:
            Validated codec value

        Raises:
            ValueError: If codec is not supported
        """
        valid_codecs = ["aac", "mp3", "opus", "ac3"]
        if v not in valid_codecs:
            raise ValueError(
                f"Invalid codec '{v}'. Choose from: {', '.join(valid_codecs)}"
            )
        return v

    @field_validator("bitrate")
    @classmethod
    def validate_bitrate(cls, v: str) -> str:
        """Validate audio bitrate format.

        Args:
            v: Bitrate value to validate

        Returns:
            Validated bitrate value

        Raises:
            ValueError: If bitrate format is invalid
        """
        if not v.endswith("k") and not v.endswith("M"):
            raise ValueError(
                f"Invalid bitrate format '{v}'. Must end with 'k' or 'M' (e.g., '128k', '0.5M')"
            )
        return v


class SubtitleConfig(BaseModel):
    """Subtitle processing settings.

    Attributes:
        enabled: Whether to burn subtitles into video
        language: Preferred subtitle language (e.g., 'eng', 'tha')
        force_style: Custom subtitle style overrides
    """

    enabled: bool = Field(
        default=True,
        description="Enable subtitle burning"
    )
    language: Optional[str] = Field(
        default=None,
        description="Preferred subtitle language code"
    )
    force_style: Optional[str] = Field(
        default=None,
        description="Custom subtitle style"
    )


class Config(BaseSettings):
    """Main configuration model.

    This class manages all settings for the MKV to MP4 batch converter,
    including paths, encoding settings, and processing options.

    Attributes:
        input_folder: Directory containing source MKV files
        output_folder: Directory for converted MP4 files
        logs_folder: Directory for log files
        video: Video encoding configuration
        audio: Audio encoding configuration
        subtitles: Subtitle processing configuration
        parallel_processing: Enable parallel file processing
        max_workers: Maximum number of parallel workers
        skip_existing: Skip files that have already been converted
        verbose: Enable verbose logging
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="CONVERTER_",
        case_sensitive=False
    )

    # Directory settings
    input_folder: Path = Field(
        default=Path("input"),
        description="Input folder for MKV files"
    )
    output_folder: Path = Field(
        default=Path("output"),
        description="Output folder for MP4 files"
    )
    logs_folder: Path = Field(
        default=Path("logs"),
        description="Logs folder"
    )

    # Encoding settings
    video: VideoConfig = Field(
        default_factory=VideoConfig,
        description="Video encoding settings"
    )
    audio: AudioConfig = Field(
        default_factory=AudioConfig,
        description="Audio encoding settings"
    )
    subtitles: SubtitleConfig = Field(
        default_factory=SubtitleConfig,
        description="Subtitle settings"
    )

    # Processing options
    parallel_processing: bool = Field(
        default=False,
        description="Enable parallel processing"
    )
    max_workers: int = Field(
        default=2,
        ge=1,
        le=16,
        description="Maximum parallel workers"
    )
    skip_existing: bool = Field(
        default=True,
        description="Skip already converted files"
    )
    verbose: bool = Field(
        default=False,
        description="Enable verbose logging"
    )

    def ensure_directories(self) -> None:
        """Create required directories if they don't exist.

        Creates input, output, and logs directories with proper permissions.
        """
        self.input_folder.mkdir(parents=True, exist_ok=True)
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.logs_folder.mkdir(parents=True, exist_ok=True)


def load_config(config_path: str | Path = "config.yaml") -> Config:
    """Load and validate configuration from YAML file.

    Args:
        config_path: Path to the YAML configuration file

    Returns:
        Validated Config object

    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file has invalid YAML syntax
        pydantic.ValidationError: If config values are invalid

    Examples:
        >>> config = load_config("config.yaml")
        >>> print(config.video.resolution)
        480
    """
    config_file = Path(config_path)

    if not config_file.exists():
        # Return default configuration
        print(f"Warning: Config file '{config_path}' not found. Using default configuration.")
        return Config()

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)

        if config_data is None:
            config_data = {}

        return Config(**config_data)

    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in config file: {e}") from e


def save_config(config: Config, config_path: str | Path = "config.yaml") -> None:
    """Save configuration to YAML file.

    Args:
        config: Config object to save
        config_path: Path where to save the configuration

    Examples:
        >>> config = Config()
        >>> config.video.resolution = 720
        >>> save_config(config, "config.yaml")
    """
    config_file = Path(config_path)

    # Convert config to dict
    config_dict = {
        "input_folder": str(config.input_folder),
        "output_folder": str(config.output_folder),
        "logs_folder": str(config.logs_folder),
        "video": {
            "resolution": config.video.resolution,
            "codec": config.video.codec,
            "crf": config.video.crf,
            "preset": config.video.preset,
        },
        "audio": {
            "codec": config.audio.codec,
            "bitrate": config.audio.bitrate,
        },
        "subtitles": {
            "enabled": config.subtitles.enabled,
            "language": config.subtitles.language,
            "force_style": config.subtitles.force_style,
        },
        "parallel_processing": config.parallel_processing,
        "max_workers": config.max_workers,
        "skip_existing": config.skip_existing,
        "verbose": config.verbose,
    }

    with open(config_file, "w", encoding="utf-8") as f:
        yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False, indent=2)
