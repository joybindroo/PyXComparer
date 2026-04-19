#!/usr/bin/env python3
"""PyXComparer - Entry point for GUI application.

This is a thin wrapper that launches the GUI application.
For CLI usage, use: pyxcomparer --help
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from pyxcomparer.gui import PyXComparerApp


def main():
    """Run the PyXComparer GUI application."""
    app = PyXComparerApp()
    app.run()


if __name__ == "__main__":
    main()
