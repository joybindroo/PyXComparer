# Changelog

All notable changes to PyXComparer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-04-18

### ✨ Added
- **CLI interface** - Full command-line interface with Click framework
  - `compare` command for comparing two XLSForms
  - `metadata` command for generating data dictionaries
  - `batch` command for processing multiple form pairs
  - `summary` command for quick change statistics
- **Multiple output formats** - HTML, JSON, YAML reports
- **Type hints** - Python 3.10+ type annotations throughout codebase
- **Custom exceptions** - Dedicated exception classes for error handling
- **Configuration module** - Centralized configuration with dataclass
- **Unit tests** - Pytest test suite for converter and comparator modules
- **Package structure** - Proper Python package layout in `src/` directory
- **pyproject.toml** - Modern Python project metadata and dependency management
- **Documentation** - Comprehensive README with usage examples

### 🔧 Changed
- **Modularized codebase** - Split monolithic script into separate modules:
  - `converter.py` - XLSForm to YAML conversion
  - `comparator.py` - File comparison logic
  - `reporter.py` - Report generation
  - `gui/main_window.py` - GUI application
- **Improved error handling** - Specific exceptions with clear messages
- **Better naming** - Consistent snake_case conventions
- **Enhanced logging** - Verbose mode in CLI for debugging

### 📦 Dependencies
- Added `click>=8.0.0` for CLI
- Updated `pandas>=2.2.0`
- Updated `numpy>=1.26.0`
- Updated `openpyxl>=3.1.0`

### 🧪 Development
- Added `pytest` and `pytest-cov` for testing
- Added `black`, `flake8`, `isort` for code quality
- Added `mypy` for type checking
- Added `pre-commit` hooks configuration

### 📝 Documentation
- Added CHANGELOG.md
- Updated README.md with CLI examples
- Added API usage section
- Added development setup instructions

---

## [1.0.0] - 2024-05-01

### ✨ Added
- Initial release
- GUI-based XLSForm comparison
- YAML metadata generation
- HTML diff report export
- Support for ODK XLSForm format (survey, choices, settings sheets)
- Color-coded diff visualization
- Hindi font support in GUI

### 🙏 Acknowledgements
- Inspired by ODK community needs
- Created for large survey projects with multiple contributors

---

## Future Releases (Planned)

### [1.2.0] - Planned
- PDF report export
- Side-by-side GUI diff view
- Progress bars for large forms
- Recent files history in GUI

### [1.3.0] - Planned
- Change categorization by type (question, choice, validation)
- Advanced filtering of changes
- Integration with ODK Central API
- Automated changelog generation

### [2.0.0] - Future
- Web-based interface option
- Real-time collaboration features
- Cloud storage integration
- Advanced analytics dashboard
