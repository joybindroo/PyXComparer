"""Command-line interface for PyXComparer."""

import sys
from pathlib import Path
from typing import Optional

import click

from pyxcomparer import convert_xlsform_to_yaml, compare_yaml_files, generate_html_report
from pyxcomparer.reporter import generate_json_report, generate_summary_report
from pyxcomparer.comparator import get_diff_summary
from pyxcomparer.exceptions import XLSFormError, XLSFormNotFoundError
from pyxcomparer.config import config


@click.group()
@click.version_option(version="1.1.0", prog_name="PyXComparer")
def main():
    """PyXComparer - Compare different versions of ODK XLSForms.

    A tool for monitoring changes between XLSForm versions and generating
    human-readable reports.
    """
    pass


@main.command()
@click.argument("old_form", type=click.Path(exists=True))
@click.argument("new_form", type=click.Path(exists=True))
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    default=None,
    help="Output HTML report path (default: auto-generated)",
)
@click.option(
    "-f",
    "--format",
    type=click.Choice(["html", "json", "all"]),
    default="html",
    help="Output format (default: html)",
)
@click.option(
    "--yaml-dir",
    type=click.Path(),
    default=None,
    help="Directory to store intermediate YAML files",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Enable verbose output",
)
def compare(
    old_form: str,
    new_form: str,
    output: Optional[str],
    format: str,
    yaml_dir: Optional[str],
    verbose: bool,
):
    """Compare two XLSForm files and generate a diff report.

    OLD_FORM: Path to older XLSForm file (.xlsx)

    NEW_FORM: Path to newer XLSForm file (.xlsx)

    Examples:

        pyxcomparer compare survey_v1.xlsx survey_v2.xlsx

        pyxcomparer compare old.xlsx new.xlsx -o report.html -v

        pyxcomparer compare form1.xlsx form2.xlsx --format all
    """
    try:
        click.echo(f"Comparing XLSForms...")
        click.echo(f"  Old: {old_form}")
        click.echo(f"  New: {new_form}")

        # Convert to YAML
        yaml_dir_path = Path(yaml_dir) if yaml_dir else None
        yaml1 = convert_xlsform_to_yaml(old_form, output_dir=yaml_dir_path)
        yaml2 = convert_xlsform_to_yaml(new_form, output_dir=yaml_dir_path)

        if verbose:
            click.echo(f"  YAML 1: {yaml1}")
            click.echo(f"  YAML 2: {yaml2}")

        # Get summary
        summary = get_diff_summary(yaml1, yaml2)
        click.echo(f"\nChanges detected:")
        click.echo(f"  Total: {summary['total_changes']}")
        click.echo(f"  Additions: {summary['additions']}")
        click.echo(f"  Deletions: {summary['deletions']}")
        click.echo(f"  Modifications: {summary['modifications']}")

        # Generate reports
        output_path = Path(output) if output else None

        if format in ["html", "all"]:
            html_path = generate_html_report(yaml1, yaml2, output_path)
            click.echo(f"\n✓ HTML report: {html_path}")

        if format in ["json", "all"]:
            json_path = generate_json_report(yaml1, yaml2)
            click.echo(f"✓ JSON report: {json_path}")

        click.echo("\nComparison complete!")

    except XLSFormNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except XLSFormError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@main.command()
@click.argument("xlsform", type=click.Path(exists=True))
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    default=None,
    help="Output YAML file path",
)
@click.option(
    "-f",
    "--format",
    type=click.Choice(["yaml", "json"]),
    default="yaml",
    help="Output format (default: yaml)",
)
@click.option(
    "--no-choices",
    is_flag=True,
    help="Exclude choice lists from metadata",
)
def metadata(xlsform: str, output: Optional[str], format: str, no_choices: bool):
    """Generate metadata/data dictionary from XLSForm.

    XLSFORM: Path to XLSForm file (.xlsx)

    Examples:

        pyxcomparer metadata survey.xlsx

        pyxcomparer metadata form.xlsx -o metadata.yaml

        pyxcomparer metadata survey.xlsx --format json
    """
    try:
        click.echo(f"Generating metadata for: {xlsform}")

        output_path = Path(output) if output else None
        if format == "json" and output_path and output_path.suffix != ".json":
            output_path = output_path.with_suffix(".json")

        yaml_path = convert_xlsform_to_yaml(
            xlsform,
            output_path=output_path if format == "yaml" else None,
            include_choices=not no_choices,
        )

        click.echo(f"✓ YAML metadata: {yaml_path}")

        if format == "json":
            import yaml
            import json

            with open(yaml_path, "r", encoding="utf-8") as f:
                yaml_data = list(yaml.safe_load_all(f))

            json_path = yaml_path.with_suffix(".json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(yaml_data, f, indent=2, ensure_ascii=False)

            click.echo(f"✓ JSON metadata: {json_path}")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("forms_dir", type=click.Path(exists=True))
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(),
    default=None,
    help="Output directory for reports",
)
@click.option(
    "--pattern",
    default="*.xlsx",
    help="File pattern to match (default: *.xlsx)",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Enable verbose output",
)
def batch(forms_dir: str, output_dir: Optional[str], pattern: str, verbose: bool):
    """Batch compare multiple XLSForm pairs.

    FORMS_DIR: Directory containing XLSForm files

    This command looks for pairs of files with similar names and compares them.
    File pairs are identified by common prefixes (e.g., survey_v1.xlsx and survey_v2.xlsx).

    Examples:

        pyxcomparer batch ./forms/

        pyxcomparer batch ./surveys/ -o ./reports/ -v
    """
    try:
        forms_path = Path(forms_dir)
        output_path = Path(output_dir) if output_dir else forms_path / "reports"
        output_path.mkdir(parents=True, exist_ok=True)

        # Find all XLSForm files
        xlsx_files = sorted(forms_path.glob(pattern))

        if not xlsx_files:
            click.echo(f"No XLSForm files found matching '{pattern}'")
            return

        click.echo(f"Found {len(xlsx_files)} XLSForm files")
        click.echo(f"Output directory: {output_path}")

        # Group files by base name (simple pairing logic)
        # This is a basic implementation - can be enhanced
        compared = 0
        for i in range(0, len(xlsx_files) - 1, 2):
            file1 = xlsx_files[i]
            file2 = xlsx_files[i + 1]

            click.echo(f"\nComparing: {file1.name} vs {file2.name}")

            try:
                yaml1 = convert_xlsform_to_yaml(file1, output_dir=output_path)
                yaml2 = convert_xlsform_to_yaml(file2, output_dir=output_path)

                summary = get_diff_summary(yaml1, yaml2)
                click.echo(f"  Changes: {summary['total_changes']}")

                report_name = f"{file1.stem}_vs_{file2.stem}_report.html"
                report_path = output_path / report_name
                generate_html_report(yaml1, yaml2, output_path=report_path)

                click.echo(f"  ✓ Report: {report_path.name}")
                compared += 1

            except Exception as e:
                click.echo(f"  Error: {e}", err=True)
                if verbose:
                    import traceback
                    traceback.print_exc()

        click.echo(f"\nBatch complete: {compared} comparisons performed")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("old_form", type=click.Path(exists=True))
@click.argument("new_form", type=click.Path(exists=True))
def summary(old_form: str, new_form: str):
    """Show quick summary of changes between two forms.

    OLD_FORM: Path to older XLSForm file

    NEW_FORM: Path to newer XLSForm file

    Example:

        pyxcomparer summary v1.xlsx v2.xlsx
    """
    try:
        yaml1 = convert_xlsform_to_yaml(old_form)
        yaml2 = convert_xlsform_to_yaml(new_form)

        summary = get_diff_summary(yaml1, yaml2)

        click.echo(f"\nChanges: {old_form} → {new_form}")
        click.echo("-" * 40)
        click.echo(f"Total:         {summary['total_changes']}")
        click.echo(f"Additions:     {summary['additions']}")
        click.echo(f"Deletions:     {summary['deletions']}")
        click.echo(f"Modifications: {summary['modifications']}")
        click.echo()

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
