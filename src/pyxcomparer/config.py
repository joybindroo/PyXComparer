"""Configuration for PyXComparer."""

from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """PyXComparer configuration."""

    # Output formats
    DEFAULT_OUTPUT_FORMAT: str = "html"
    SUPPORTED_FORMATS: tuple = ("html", "json", "yaml")

    # File settings
    DEFAULT_OUTPUT_FILENAME: str = "form_diff_report.html"
    YAML_EXTENSION: str = ".yaml"
    XLSX_EXTENSION: str = ".xlsx"

    # XLSForm sheet names
    SURVEY_SHEET: str = "survey"
    CHOICES_SHEET: str = "choices"
    SETTINGS_SHEET: str = "settings"

    # Display settings
    DEFAULT_FONT: str = "Arial"
    HINDI_FONT: str = "Mangal"
    GUI_WIDTH: int = 80
    GUI_HEIGHT: int = 30

    # Diff settings
    DIFF_WRAP_COLUMN: int = 80
    MAX_CHOICES_DISPLAY: Optional[int] = 25

    # Colors for diff display
    COLOR_ADDED: str = "green"
    COLOR_DELETED: str = "red"
    COLOR_MODIFIED: str = "blue"

    # Settings fields to extract
    SETTINGS_FIELDS: tuple = ("form_title", "form_id")

    @classmethod
    def get_output_path(
        cls,
        input_path: Path | str,
        output_dir: Optional[Path | str] = None,
        suffix: str = "_diff",
    ) -> Path:
        """Generate output file path based on input.

        Args:
            input_path: Path to input file
            output_dir: Optional output directory
            suffix: Suffix to add to filename

        Returns:
            Path object for output file
        """
        input_path = Path(input_path)
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        else:
            output_dir = input_path.parent

        stem = input_path.stem.replace(".", "_")
        return output_dir / f"{stem}{suffix}{cls.YAML_EXTENSION}"


# Global config instance
config = Config()
