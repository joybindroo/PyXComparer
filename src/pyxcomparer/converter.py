"""XLSForm to YAML converter module.

Converts ODK XLSForm Excel files to human-readable YAML metadata.
"""

from pathlib import Path
from typing import Optional
import pandas as pd
import yaml

from pyxcomparer.config import config
from pyxcomparer.exceptions import XLSFormError, XLSFormNotFoundError


def convert_xlsform_to_yaml(
    input_path: Path | str,
    output_path: Optional[Path | str] = None,
    include_choices: bool = True,
    max_choices: int = 30,
) -> Path:
    """Convert XLSForm survey to YAML metadata.

    Extracts survey structure, choices, and settings from an ODK XLSForm
    Excel file and converts it to a human-readable YAML format.

    Args:
        input_path: Path to .xlsx XLSForm file
        output_path: Path for output YAML file (auto-generated if None)
        include_choices: Include choice lists in output
        max_choices: Maximum number of choices to include per list

    Returns:
        Path to generated YAML file

    Raises:
        XLSFormNotFoundError: If input file doesn't exist
        XLSFormError: If required sheets are missing or file is invalid

    Example:
        >>> yaml_path = convert_xlsform_to_yaml("survey_v1.xlsx")
        >>> print(yaml_path)
        survey_v1_yaml.yaml
    """
    input_path = Path(input_path)

    # Validate input file
    if not input_path.exists():
        raise XLSFormNotFoundError(f"XLSForm file not found: {input_path}")

    if input_path.suffix.lower() != config.XLSX_EXTENSION:
        raise XLSFormError(
            f"Invalid file format. Expected {config.XLSX_EXTENSION}, "
            f"got {input_path.suffix}"
        )

    # Generate output path if not provided
    if output_path is None:
        output_path = config.get_output_path(input_path, suffix="_yaml")
    else:
        output_path = Path(output_path)

    try:
        # Read XLSForm sheets
        df_survey = _read_sheet(input_path, config.SURVEY_SHEET)
        df_choices = _read_sheet(input_path, config.CHOICES_SHEET) if include_choices else None
        df_settings = _read_sheet(input_path, config.SETTINGS_SHEET)

        # Build metadata structure
        metadata = _build_metadata(df_survey, df_choices, df_settings, max_choices)

        # Write YAML file
        _write_yaml(metadata, output_path)

        return output_path

    except Exception as e:
        raise XLSFormError(f"Failed to convert XLSForm: {e}") from e


def _read_sheet(file_path: Path, sheet_name: str) -> pd.DataFrame:
    """Read a sheet from XLSForm file.

    Args:
        file_path: Path to XLSForm file
        sheet_name: Name of sheet to read

    Returns:
        DataFrame with sheet contents

    Raises:
        XLSFormError: If sheet is missing
    """
    try:
        return pd.read_excel(file_path, sheet_name=sheet_name)
    except ValueError as e:
        if "sheet named" in str(e):
            raise XLSFormError(
                f"Required sheet '{sheet_name}' not found in {file_path.name}"
            ) from e
        raise


def _build_metadata(
    df_survey: pd.DataFrame,
    df_choices: Optional[pd.DataFrame],
    df_settings: pd.DataFrame,
    max_choices: int,
) -> list[dict]:
    """Build metadata structure from XLSForm data.

    Args:
        df_survey: Survey sheet DataFrame
        df_choices: Choices sheet DataFrame (optional)
        df_settings: Settings sheet DataFrame
        max_choices: Maximum choices to include per list

    Returns:
        List of metadata dictionaries
    """
    metadata = []

    # Extract settings
    settings_data = _extract_settings(df_settings)
    if settings_data:
        metadata.append(settings_data)

    # Extract survey questions
    for idx in range(len(df_survey)):
        question_data = _extract_question(df_survey, idx, df_choices, max_choices)
        if question_data:
            metadata.append(question_data)

    return metadata


def _extract_settings(df_settings: pd.DataFrame) -> dict:
    """Extract settings from settings sheet.

    Args:
        df_settings: Settings sheet DataFrame

    Returns:
        Dictionary with form metadata
    """
    settings = {}

    for field in config.SETTINGS_FIELDS:
        if field in df_settings.columns:
            value = df_settings[field].iloc[0] if len(df_settings) > 0 else None
            if pd.notna(value):
                settings[field] = value

    return settings if settings else {}


def _extract_question(
    df_survey: pd.DataFrame,
    idx: int,
    df_choices: Optional[pd.DataFrame],
    max_choices: int,
) -> dict:
    """Extract question metadata from survey row.

    Args:
        df_survey: Survey sheet DataFrame
        idx: Row index
        df_choices: Choices sheet DataFrame
        max_choices: Maximum choices to include

    Returns:
        Dictionary with question metadata
    """
    row = df_survey.iloc[idx]
    question_data = row.dropna().to_dict()

    # Extract choice list if applicable
    if df_choices is not None and "type" in question_data:
        type_value = str(question_data.get("type", ""))
        tokens = type_value.split()

        if len(tokens) > 1:
            list_name = tokens[1]
            choices_data = _extract_choices(df_choices, list_name, max_choices)
            if choices_data:
                key = f"Option_List::{list_name}"
                question_data[key] = choices_data

    return question_data if question_data else {}


def _extract_choices(
    df_choices: pd.DataFrame,
    list_name: str,
    max_choices: int,
) -> dict:
    """Extract choices for a specific list.

    Args:
        df_choices: Choices sheet DataFrame
        list_name: Name of choice list
        max_choices: Maximum number of choices to include

    Returns:
        Dictionary with choice options
    """
    if list_name not in df_choices["list_name"].values:
        return {}

    choices_df = df_choices[df_choices["list_name"] == list_name][["name", "label"]]
    choices_df = choices_df.head(max_choices)
    choices_df.columns = ["Code", "Label"]
    choices_df.index = [f"Option{i+1}" for i in range(len(choices_df))]

    return choices_df.T.to_dict()


def _write_yaml(metadata: list[dict], output_path: Path) -> None:
    """Write metadata to YAML file.

    Args:
        metadata: List of metadata dictionaries
        output_path: Path to output file
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for item in metadata:
            yaml.dump(
                [item],
                f,
                allow_unicode=True,
                default_flow_style=False,
                sort_keys=False,
                indent=4,
            )
            f.write("\n")
