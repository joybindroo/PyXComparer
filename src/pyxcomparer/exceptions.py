"""Custom exceptions for PyXComparer."""


class XLSFormError(Exception):
    """Base exception for XLSForm-related errors."""

    pass


class XLSFormNotFoundError(XLSFormError):
    """Raised when XLSForm file is not found."""

    pass


class InvalidXLSFormError(XLSFormError):
    """Raised when XLSForm structure is invalid."""

    pass


class ConversionError(XLSFormError):
    """Raised when XLSForm to YAML conversion fails."""

    pass


class ComparisonError(Exception):
    """Base exception for comparison-related errors."""

    pass


class FileReadError(ComparisonError):
    """Raised when file cannot be read."""

    pass


class ReportGenerationError(Exception):
    """Raised when report generation fails."""

    pass
