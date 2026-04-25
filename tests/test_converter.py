"""Unit tests for PyXComparer converter module."""

import pytest
from pathlib import Path
import tempfile
import pandas as pd
import yaml

from pyxcomparer.converter import convert_xlsform_to_yaml
from pyxcomparer.exceptions import XLSFormError, XLSFormNotFoundError


@pytest.fixture
def sample_xlsform(tmp_path: Path) -> Path:
    """Create a sample XLSForm for testing."""
    # Create sample survey sheet
    survey_data = {
        "type": ["text", "select_one yes_no", "integer"],
        "name": ["q1", "q2", "q3"],
        "label": ["Question 1", "Question 2", "Question 3"],
        "required": [False, True, False],
    }
    df_survey = pd.DataFrame(survey_data)

    # Create sample choices sheet
    choices_data = {
        "list_name": ["yes_no", "yes_no"],
        "name": ["yes", "no"],
        "label": ["Yes", "No"],
    }
    df_choices = pd.DataFrame(choices_data)

    # Create sample settings sheet
    settings_data = {
        "form_title": ["Test Form"],
        "form_id": ["test_form_v1"],
    }
    df_settings = pd.DataFrame(settings_data)

    # Write to Excel file
    output_file = tmp_path / "test_form.xlsx"
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        df_survey.to_excel(writer, sheet_name="survey", index=False)
        df_choices.to_excel(writer, sheet_name="choices", index=False)
        df_settings.to_excel(writer, sheet_name="settings", index=False)

    return output_file


class TestConvertXLSFormToYAML:
    """Tests for convert_xlsform_to_yaml function."""

    def test_convert_valid_xlsform(self, sample_xlsform: Path, tmp_path: Path):
        """Test conversion of valid XLSForm."""
        output_path = tmp_path / "output.yaml"
        result = convert_xlsform_to_yaml(sample_xlsform, output_path)

        assert result.exists()
        assert result.suffix == ".yaml"

        # Verify YAML content
        with open(result, "r", encoding="utf-8") as f:
            data = list(yaml.safe_load_all(f))

        assert len(data) > 0
        assert any("form_title" in str(item) for item in data)

    def test_convert_missing_file(self, tmp_path: Path):
        """Test conversion with missing input file."""
        missing_file = tmp_path / "missing.xlsx"

        with pytest.raises(XLSFormNotFoundError):
            convert_xlsform_to_yaml(missing_file)

    def test_convert_invalid_extension(self, tmp_path: Path):
        """Test conversion with invalid file extension."""
        invalid_file = tmp_path / "test.csv"
        invalid_file.write_text("dummy content")

        with pytest.raises(XLSFormError):
            convert_xlsform_to_yaml(invalid_file)

    def test_convert_auto_output_path(self, sample_xlsform: Path, tmp_path: Path):
        """Test auto-generation of output path."""
        import shutil

        # Copy file to test auto-path generation
        test_file = tmp_path / "test_survey.xlsx"
        shutil.copy(sample_xlsform, test_file)

        result = convert_xlsform_to_yaml(test_file)

        assert result.exists()
        assert result.name.startswith("test_survey_yaml")
        assert result.suffix == ".yaml"

    def test_convert_without_choices(
        self, sample_xlsform: Path, tmp_path: Path
    ):
        """Test conversion without including choices."""
        output_path = tmp_path / "output_no_choices.yaml"
        result = convert_xlsform_to_yaml(
            sample_xlsform, output_path, include_choices=False
        )

        assert result.exists()

        with open(result, "r", encoding="utf-8") as f:
            content = f.read()

        assert "Option_List" not in content

    def test_convert_with_max_choices(
        self, sample_xlsform: Path, tmp_path: Path
    ):
        """Test conversion with max_choices limit."""
        output_path = tmp_path / "output_limited.yaml"
        result = convert_xlsform_to_yaml(
            sample_xlsform, output_path, max_choices=1
        )

        assert result.exists()

        with open(result, "r", encoding="utf-8") as f:
            data = list(yaml.safe_load_all(f))

        # Check that choices are limited
        for item in data:
            for key, value in item.items():
                if key.startswith("Option_List"):
                    assert len(value) <= 1
