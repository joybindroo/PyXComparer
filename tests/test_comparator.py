"""Unit tests for PyXComparer comparator module."""

import pytest
from pathlib import Path
import tempfile

from pyxcomparer.comparator import (
    compare_yaml_files,
    get_diff_summary,
)
from pyxcomparer.exceptions import FileReadError


@pytest.fixture
def sample_yaml_files(tmp_path: Path) -> tuple[Path, Path]:
    """Create sample YAML files for testing."""
    yaml1_content = """---
- form_title: Test Form
  form_id: test_v1
---
- type: text
  name: q1
  label: Question 1
---
- type: integer
  name: q2
  label: Question 2
"""

    yaml2_content = """---
- form_title: Test Form
  form_id: test_v1
---
- type: text
  name: q1
  label: Question 1 Updated
---
- type: integer
  name: q2
  label: Question 2
---
- type: select_one yes
  name: q3
  label: Question 3 New
"""

    file1 = tmp_path / "form_v1.yaml"
    file2 = tmp_path / "form_v2.yaml"

    file1.write_text(yaml1_content, encoding="utf-8")
    file2.write_text(yaml2_content, encoding="utf-8")

    return file1, file2


class TestCompareYAMLFiles:
    """Tests for compare_yaml_files function."""

    def test_compare_text_format(self, sample_yaml_files: tuple[Path, Path]):
        """Test comparison with text output format."""
        file1, file2 = sample_yaml_files
        result = compare_yaml_files(file1, file2, output_format="text")

        assert isinstance(result, list)
        assert len(result) > 0
        assert any(line.startswith("+") for line in result)
        assert any(line.startswith("-") for line in result)

    def test_compare_html_format(self, sample_yaml_files: tuple[Path, Path]):
        """Test comparison with HTML output format."""
        file1, file2 = sample_yaml_files
        result = compare_yaml_files(file1, file2, output_format="html")

        assert isinstance(result, str)
        assert "<html>" in result.lower()
        assert "<table" in result.lower()

    def test_compare_dict_format(self, sample_yaml_files: tuple[Path, Path]):
        """Test comparison with dict output format."""
        file1, file2 = sample_yaml_files
        result = compare_yaml_files(file1, file2, output_format="dict")

        assert isinstance(result, dict)
        assert "added" in result
        assert "deleted" in result
        assert "modified" in result
        assert "unchanged" in result

    def test_compare_missing_file(self, tmp_path: Path):
        """Test comparison with missing file."""
        existing_file = tmp_path / "exists.yaml"
        existing_file.write_text("test", encoding="utf-8")
        missing_file = tmp_path / "missing.yaml"

        with pytest.raises(FileReadError):
            compare_yaml_files(existing_file, missing_file)

    def test_compare_identical_files(self, tmp_path: Path):
        """Test comparison of identical files."""
        content = "---\n- test: value\n"
        file1 = tmp_path / "file1.yaml"
        file2 = tmp_path / "file2.yaml"

        file1.write_text(content, encoding="utf-8")
        file2.write_text(content, encoding="utf-8")

        result = compare_yaml_files(file1, file2, output_format="dict")

        assert len(result["added"]) == 0
        assert len(result["deleted"]) == 0
        assert len(result["modified"]) == 0


class TestGetDiffSummary:
    """Tests for get_diff_summary function."""

    def test_summary_statistics(self, sample_yaml_files: tuple[Path, Path]):
        """Test summary statistics calculation."""
        file1, file2 = sample_yaml_files
        summary = get_diff_summary(file1, file2)

        assert isinstance(summary, dict)
        assert "total_changes" in summary
        assert "additions" in summary
        assert "deletions" in summary
        assert "modifications" in summary

        assert summary["total_changes"] == (
            summary["additions"]
            + summary["deletions"]
            + summary["modifications"]
        )

    def test_summary_no_changes(self, tmp_path: Path):
        """Test summary with no changes."""
        content = "---\n- test: value\n"
        file1 = tmp_path / "file1.yaml"
        file2 = tmp_path / "file2.yaml"

        file1.write_text(content, encoding="utf-8")
        file2.write_text(content, encoding="utf-8")

        summary = get_diff_summary(file1, file2)

        assert summary["total_changes"] == 0
        assert summary["additions"] == 0
        assert summary["deletions"] == 0
        assert summary["modifications"] == 0

    def test_summary_with_additions(self, tmp_path: Path):
        """Test summary with additions only."""
        file1 = tmp_path / "file1.yaml"
        file2 = tmp_path / "file2.yaml"

        file1.write_text("---\n- test: value1\n", encoding="utf-8")
        file2.write_text("---\n- test: value1\n- new: item\n", encoding="utf-8")

        summary = get_diff_summary(file1, file2)

        assert summary["additions"] > 0
        assert summary["deletions"] == 0
