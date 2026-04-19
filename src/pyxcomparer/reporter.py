"""Report generation module.

Generates HTML, JSON, and other format reports from XLSForm comparisons.
"""

from pathlib import Path
from typing import Optional, Literal
import json
from datetime import datetime

from pyxcomparer.comparator import compare_yaml_files, get_diff_summary
from pyxcomparer.exceptions import ReportGenerationError


def generate_html_report(
    yaml_file1: Path | str,
    yaml_file2: Path | str,
    output_path: Optional[Path | str] = None,
    title: Optional[str] = None,
) -> Path:
    """Generate HTML diff report.

    Args:
        yaml_file1: Path to first YAML file (older version)
        yaml_file2: Path to second YAML file (newer version)
        output_path: Path for output HTML file (auto-generated if None)
        title: Custom title for report

    Returns:
        Path to generated HTML report

    Raises:
        ReportGenerationError: If report generation fails

    Example:
        >>> report_path = generate_html_report("form_v1.yaml", "form_v2.yaml")
        >>> print(f"Report saved: {report_path}")
    """
    try:
        # Generate HTML diff
        html_content = compare_yaml_files(
            yaml_file1, yaml_file2, output_format="html"
        )

        # Add custom title if provided
        if title:
            html_content = _inject_title(html_content, title)

        # Determine output path
        if output_path is None:
            output_path = _get_default_output_path(yaml_file2, ".html")
        else:
            output_path = Path(output_path)

        # Write report
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html_content, encoding="utf-8")

        return output_path

    except Exception as e:
        raise ReportGenerationError(f"Failed to generate HTML report: {e}") from e


def generate_json_report(
    yaml_file1: Path | str,
    yaml_file2: Path | str,
    output_path: Optional[Path | str] = None,
    include_summary: bool = True,
) -> Path:
    """Generate JSON report with categorized changes.

    Args:
        yaml_file1: Path to first YAML file
        yaml_file2: Path to second YAML file
        output_path: Path for output JSON file
        include_summary: Include summary statistics

    Returns:
        Path to generated JSON report
    """
    try:
        # Get categorized diff
        categories = compare_yaml_files(
            yaml_file1, yaml_file2, output_format="dict"
        )

        # Build report structure
        report = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "file1": str(Path(yaml_file1)),
                "file2": str(Path(yaml_file2)),
            },
            "changes": categories,
        }

        if include_summary:
            report["summary"] = get_diff_summary(yaml_file1, yaml_file2)

        # Determine output path
        if output_path is None:
            output_path = _get_default_output_path(yaml_file2, ".json")
        else:
            output_path = Path(output_path)

        # Write report
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        return output_path

    except Exception as e:
        raise ReportGenerationError(f"Failed to generate JSON report: {e}") from e


def generate_summary_report(
    yaml_file1: Path | str,
    yaml_file2: Path | str,
    output_path: Optional[Path | str] = None,
    format: Literal["text", "markdown"] = "text",
) -> Path:
    """Generate summary report with change statistics.

    Args:
        yaml_file1: Path to first YAML file
        yaml_file2: Path to second YAML file
        output_path: Path for output file
        format: Output format - 'text' or 'markdown'

    Returns:
        Path to generated summary report
    """
    try:
        summary = get_diff_summary(yaml_file1, yaml_file2)

        if format == "markdown":
            content = _format_summary_markdown(summary, yaml_file1, yaml_file2)
        else:
            content = _format_summary_text(summary, yaml_file1, yaml_file2)

        # Determine output path
        if output_path is None:
            output_path = _get_default_output_path(yaml_file2, ".txt")
        else:
            output_path = Path(output_path)

        # Write report
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")

        return output_path

    except Exception as e:
        raise ReportGenerationError(f"Failed to generate summary report: {e}") from e


def _inject_title(html_content: str, title: str) -> str:
    """Inject custom title into HTML report.

    Args:
        html_content: Original HTML content
        title: New title

    Returns:
        Modified HTML content
    """
    return html_content.replace(
        "<title>File Difference</title>",
        f"<title>{title}</title>",
    ).replace(
        "<h2>File Difference</h2>",
        f"<h2>{title}</h2>",
    )


def _get_default_output_path(reference_file: Path | str, extension: str) -> Path:
    """Generate default output path.

    Args:
        reference_file: Reference file path
        extension: File extension

    Returns:
        Default output path
    """
    reference_path = Path(reference_file)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return reference_path.parent / f"{reference_path.stem}_report_{timestamp}{extension}"


def _format_summary_text(summary: dict, file1: Path | str, file2: Path | str) -> str:
    """Format summary as plain text.

    Args:
        summary: Summary statistics
        file1: First file path
        file2: Second file path

    Returns:
        Formatted text string
    """
    return f"""XLSForm Comparison Summary
==========================

File 1: {Path(file1).name}
File 2: {Path(file2).name}

Changes:
  Total:     {summary['total_changes']}
  Additions: {summary['additions']}
  Deletions: {summary['deletions']}
  Modifications: {summary['modifications']}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""


def _format_summary_markdown(
    summary: dict, file1: Path | str, file2: Path | str
) -> str:
    """Format summary as Markdown.

    Args:
        summary: Summary statistics
        file1: First file path
        file2: Second file path

    Returns:
        Formatted Markdown string
    """
    return f"""# XLSForm Comparison Summary

## Files Compared

- **Version 1:** `{Path(file1).name}`
- **Version 2:** `{Path(file2).name}`

## Change Statistics

| Metric | Count |
|--------|-------|
| **Total Changes** | {summary['total_changes']} |
| Additions | {summary['additions']} |
| Deletions | {summary['deletions']} |
| Modifications | {summary['modifications']} |

---
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
