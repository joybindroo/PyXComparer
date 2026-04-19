"""XLSForm comparison module.

Compares two YAML files and identifies differences.
"""

from pathlib import Path
from typing import Literal
import difflib

from pyxcomparer.exceptions import FileReadError, ComparisonError


def compare_yaml_files(
    yaml_file1: Path | str,
    yaml_file2: Path | str,
    output_format: Literal["text", "html", "dict"] = "text",
    wrap_column: int = 80,
) -> str | dict | list[str]:
    """Compare two YAML files and return differences.

    Args:
        yaml_file1: Path to first YAML file (older version)
        yaml_file2: Path to second YAML file (newer version)
        output_format: Output format - 'text', 'html', or 'dict'
        wrap_column: Column width for wrapping text in HTML output

    Returns:
        Differences in specified format:
        - text: List of diff lines with prefixes (+, -, ?, space)
        - html: HTML string with formatted diff
        - dict: Dictionary with categorized changes

    Raises:
        FileReadError: If files cannot be read
        ComparisonError: If comparison fails

    Example:
        >>> diff = compare_yaml_files("form_v1.yaml", "form_v2.yaml")
        >>> print(''.join(diff))
    """
    # Read files
    text1 = _read_file(yaml_file1)
    text2 = _read_file(yaml_file2)

    # Generate diff based on output format
    if output_format == "dict":
        return _categorize_diff(text1, text2)
    elif output_format == "html":
        return _generate_html_diff(text1, text2, wrap_column)
    else:  # text
        return _generate_text_diff(text1, text2)


def _read_file(file_path: Path | str) -> str:
    """Read file content.

    Args:
        file_path: Path to file

    Returns:
        File content as string

    Raises:
        FileReadError: If file cannot be read
    """
    try:
        return Path(file_path).read_text(encoding="utf-8")
    except FileNotFoundError as e:
        raise FileReadError(f"File not found: {file_path}") from e
    except Exception as e:
        raise FileReadError(f"Error reading file {file_path}: {e}") from e


def _generate_text_diff(text1: str, text2: str) -> list[str]:
    """Generate line-by-line text diff.

    Args:
        text1: First text content
        text2: Second text content

    Returns:
        List of diff lines with prefixes
    """
    differ = difflib.Differ()
    return list(
        differ.compare(
            text1.splitlines(keepends=True),
            text2.splitlines(keepends=True),
        )
    )


def _generate_html_diff(text1: str, text2: str, wrap_column: int = 80) -> str:
    """Generate HTML diff report.

    Args:
        text1: First text content
        text2: Second text content
        wrap_column: Column width for text wrapping

    Returns:
        HTML string with formatted diff
    """
    differ = difflib.HtmlDiff(wrapcolumn=wrap_column)
    return differ.make_file(text1.splitlines(), text2.splitlines())


def _categorize_diff(text1: str, text2: str) -> dict:
    """Categorize differences by type.

    Args:
        text1: First text content
        text2: Second text content

    Returns:
        Dictionary with categorized changes:
        {
            'added': [...],
            'deleted': [...],
            'modified': [...]
        }
    """
    diff = _generate_text_diff(text1, text2)

    categories = {
        "added": [],
        "deleted": [],
        "modified": [],
        "unchanged": [],
    }

    for line in diff:
        if line.startswith("+"):
            categories["added"].append(line[2:].strip())
        elif line.startswith("-"):
            categories["deleted"].append(line[2:].strip())
        elif line.startswith("?"):
            categories["modified"].append(line[2:].strip())
        else:
            categories["unchanged"].append(line[2:].strip())

    return categories


def get_diff_summary(yaml_file1: Path | str, yaml_file2: Path | str) -> dict:
    """Get summary statistics of differences.

    Args:
        yaml_file1: Path to first YAML file
        yaml_file2: Path to second YAML file

    Returns:
        Dictionary with summary statistics:
        {
            'total_changes': int,
            'additions': int,
            'deletions': int,
            'modifications': int
        }
    """
    categories = compare_yaml_files(yaml_file1, yaml_file2, output_format="dict")

    return {
        "total_changes": (
            len(categories["added"])
            + len(categories["deleted"])
            + len(categories["modified"])
        ),
        "additions": len(categories["added"]),
        "deletions": len(categories["deleted"]),
        "modifications": len(categories["modified"]),
    }
