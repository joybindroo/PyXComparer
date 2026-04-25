# PyXComparer

**PyXComparer** is a Python-based tool designed to simplify the process of monitoring changes between different versions of ODK XLSForms. It provides GUI, CLI, and Web interfaces for comparing XLSForm files, helping teams ensure data integrity and consistency in their survey projects.

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ Features

- **Compare XLSForm versions** - Identify changes between survey versions
- **Multiple output formats** - HTML, JSON, YAML reports
- **Three Interface Modes** - GUI, CLI, and Web (Flask)
- **Human-readable metadata** - Generate data dictionaries from XLSForms
- **Batch processing** - Compare multiple form pairs at once
- **Change categorization** - Track additions, deletions, and modifications
- **Summary statistics** - Quick overview of changes
- **Containerized** - Ready for deployment via Docker

## 🚀 Quick Start

### Installation

**Option 1: Using pip**
```bash
pip install pyxcomparer
```

**Option 2: From source**
```bash
git clone https://github.com/joybindroo/PyXComparer.git
cd PyXComparer
pip install -e .
```

**Option 3: Development mode**
```bash
git clone https://github.com/joybindroo/PyXComparer.git
cd PyXComparer
pip install -e ".[dev]"
```

### Usage

#### 🌐 Web Mode (Browser-based)
The easiest way for non-technical users to compare forms.

**Using Docker:**
```bash
docker-compose up -d
```
Then visit: `http://localhost:5000`

**Local Run:**
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python src/pyxcomparer/web/app.py
```

#### 💻 CLI Mode (Recommended for automation)

**Compare two forms:**
```bash
pyxcomparer compare survey_v1.xlsx survey_v2.xlsx
```

**Generate HTML report:**
```bash
pyxcomparer compare old.xlsx new.xlsx -o report.html --verbose
```

**Generate metadata only:**
```bash
pyxcomparer metadata survey.xlsx -o metadata.yaml
pyxcomparer metadata survey.xlsx --format json
```

**Batch compare multiple forms:**
```bash
pyxcomparer batch ./forms/ -o ./reports/
```

**Quick summary:**
```bash
pyxcomparer summary v1.xlsx v2.xlsx
```

#### 🖥️ GUI Mode

```bash
python pyxcomparer.py
```

Or from installed package:
```bash
pyxcomparer gui
```

## 📋 Workflow

```
1. Select/Input XLSForm files (.xlsx) via Web, GUI, or CLI
       ↓
2. Convert to YAML metadata (automatically)
       ↓
3. Compare YAML files
       ↓
4. Generate reports (HTML/JSON/YAML)
       ↓
5. Review changes and export
```

## 📊 Output Formats

### HTML Report
- Side-by-side diff view
- Color-coded changes (green=added, red=deleted, blue=modified)
- Browser-friendly format

### JSON Report
- Machine-readable format
- Categorized changes
- Summary statistics
- Easy to integrate with other tools

### YAML Metadata
- Human-readable data dictionary
- Extracts questions, choices, settings
- Includes validation rules and constraints

## 🏗️ Project Structure

```
PyXComparer/
├── src/pyxcomparer/
│   ├── __init__.py          # Package exports
│   ├── cli.py               # CLI interface
│   ├── config.py            # Configuration
│   ├── converter.py         # XLSForm → YAML conversion
│   ├── comparator.py        # Diff logic
│   ├── reporter.py          # Report generation
│   ├── exceptions.py        # Custom exceptions
│   ├── web/                 # Flask Web Application
│   │   └── app.py
│   └── gui/
│       ├── __init__.py
│       └── main_window.py   # GUI application
├── templates/               # Web HTML templates
├── tests/
│   ├── test_converter.py
│   └── test_comparator.py
├── pyproject.toml           # Project metadata & dependencies
├── requirements.txt         # Pip dependencies
├── Dockerfile               # Multi-stage build
├── docker-compose.yml       # Docker orchestration
└── pyxcomparer.py           # GUI entry point
```

## 🔧 Development

### Setup

```bash
# Clone repository
git clone https://github.com/joybindroo/PyXComparer.git
cd PyXComparer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pyxcomparer

# Run specific test file
pytest tests/test_converter.py -v
```

### Code Quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint
flake8 src/ tests/

# Type checking
mypy src/
```

## 📖 API Usage

### Python API

```python
from pyxcomparer import convert_xlsform_to_yaml, compare_yaml_files, generate_html_report

# Convert XLSForm to YAML
yaml_path = convert_xlsform_to_yaml("survey_v1.xlsx")

# Compare two YAML files
diff = compare_yaml_files("form_v1.yaml", "form_v2.yaml", output_format="dict")

# Generate HTML report
report_path = generate_html_report("form_v1.yaml", "form_v2.yaml", output_path="report.html")

# Get summary statistics
from pyxcomparer.comparator import get_diff_summary
summary = get_diff_summary("form_v1.yaml", "form_v2.yaml")
print(f"Total changes: {summary['total_changes']}")
```

## 🎯 Use Cases

### Public Health Surveys
Track changes in large health surveys when multiple team members collaborate on form design.

### Longitudinal Studies
Monitor modifications between survey rounds in longitudinal data collection projects.

### Multi-country Studies
Compare survey adaptations across different country contexts.

### Quality Assurance
Validate that form changes don't break existing data collection workflows.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## 🙏 Acknowledgements

PyXComparer was inspired by the need to streamline the process of managing changes between versions of ODK XLSForms when very large surveys are created by many team members and those are merged and improved over time in limited resource settings.

Special thanks to the ODK community for their support and inspiration.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

**Joy Bindroo**  
Email: joybindroo@gmail.com

## 🗂️ Related Projects

- [ODK XLSForm](https://xlsform.org/) - XLSForm standard
- [ODK Central](https://docs.getodk.org/central-intro/) - ODK server
- [pyxform](https://github.com/XLSForm/pyxform) - XLSForm to XForms converter
