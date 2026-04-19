"""Main GUI window for PyXComparer."""

import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from pathlib import Path
from typing import Optional

from pyxcomparer.converter import convert_xlsform_to_yaml
from pyxcomparer.comparator import compare_yaml_files
from pyxcomparer.reporter import generate_html_report
from pyxcomparer.config import config


class PyXComparerApp:
    """Main application window for PyXComparer."""

    def __init__(self):
        """Initialize the application."""
        self.file1: Optional[Path] = None
        self.file2: Optional[Path] = None
        self.yaml1: Optional[Path] = None
        self.yaml2: Optional[Path] = None

    def show_welcome(self) -> None:
        """Display welcome message with instructions."""
        message = """
PyXComparer (Version 1.1.0)
_____________________________________

This tool compares different versions of ODK XLSForms.

Steps:
1. Select Old Version: Choose the older XLSForm file (Form 1)
2. Select Newer Version: Choose the newer XLSForm file
3. Compare: Comparison happens automatically
4. View Differences: Review changes in a separate window
5. Save HTML Report: Export the comparison report

PyXComparer will generate:
- HTML report summarizing changes
- YAML data dictionaries for both forms

_____________________________________
Contact: joybindroo@gmail.com
_____________________________________
        """
        self._show_message(message, font=("Arial", 9))

    def run(self) -> None:
        """Run the main application workflow."""
        try:
            self.show_welcome()

            # Select files
            self.file1 = self._select_file("Select Old Version of XLSForm (.xlsx)")
            if not self.file1:
                return

            print(f">> Read: {self.file1}")

            self.file2 = self._select_file("Select New Version of XLSForm (.xlsx)")
            if not self.file2:
                return

            print(f">> Read: {self.file2}")

            # Convert to YAML
            self.yaml1 = convert_xlsform_to_yaml(self.file1)
            print(f">> Converted Form 1: {self.yaml1}")

            self.yaml2 = convert_xlsform_to_yaml(self.file2)
            print(f">> Converted Form 2: {self.yaml2}")

            # Read YAML files
            txt1 = self._read_file(self.yaml1)
            txt2 = self._read_file(self.yaml2)

            # Show diff
            self._show_diff(txt1, txt2)

            # Get output filename and generate report
            fname = self._get_output_filename()
            if fname:
                report_path = generate_html_report(
                    self.yaml1, self.yaml2, output_path=Path(fname)
                )
                self._show_message("File Saved Successfully. Click OK to exit.")
                print(f">> Report saved: {report_path}")

        except Exception as e:
            self._show_message(f"An error occurred: {str(e)}")

    def _select_file(self, title: str) -> Optional[Path]:
        """Open file selection dialog.

        Args:
            title: Dialog title

        Returns:
            Selected file path or None
        """
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title=title,
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
        )
        root.destroy()
        return Path(file_path) if file_path else None

    def _read_file(self, file_path: Path) -> str:
        """Read file content.

        Args:
            file_path: Path to file

        Returns:
            File content
        """
        return file_path.read_text(encoding="utf-8")

    def _show_message(self, message: str, font: tuple = ("Arial", 10)) -> None:
        """Display message in a dialog.

        Args:
            message: Message text
            font: Font tuple
        """
        window = tk.Tk()
        window.title("Message")
        label = tk.Label(window, text=message, justify=tk.LEFT, font=font)
        label.pack(padx=20, pady=20)

        def close_window():
            window.destroy()

        tk.Button(window, width=10, text="  OK  ", command=close_window).pack(pady=10)
        window.mainloop()

    def _show_diff(self, text1: str, text2: str) -> None:
        """Display differences in a GUI window.

        Args:
            text1: First text content
            text2: Second text content
        """
        window = tk.Tk()
        window.title("Text Difference")

        diff_text = scrolledtext.ScrolledText(window, width=80, height=30)
        diff_text.pack(expand=True, fill="both")

        diff = compare_yaml_files(
            self.yaml1,  # type: ignore
            self.yaml2,  # type: ignore
            output_format="text",
        )

        for line in diff:
            if line.startswith("+"):
                diff_text.insert(tk.END, line, "added")
            elif line.startswith("-"):
                diff_text.insert(tk.END, line, "deleted")
            elif line.startswith("?"):
                diff_text.insert(tk.END, line, "modified")
            else:
                diff_text.insert(tk.END, line)

        diff_text.tag_config("added", foreground=config.COLOR_ADDED)
        diff_text.tag_config("deleted", foreground=config.COLOR_DELETED)
        diff_text.tag_config("modified", foreground=config.COLOR_MODIFIED)

        window.mainloop()

    def _get_output_filename(self) -> Optional[str]:
        """Get output filename from user.

        Returns:
            Filename or default
        """
        root = tk.Tk()
        root.title("Save Report")

        label = tk.Label(
            root,
            text="Enter output filename (without extension):",
            font=("Arial", 9, "bold"),
        )
        label.pack()

        text_entry = tk.Entry(root, width=50)
        text_entry.pack()

        result = {"value": None}

        def save():
            result["value"] = text_entry.get()
            root.destroy()

        tk.Button(root, text="Save", command=save).pack()
        tk.Button(root, text="Cancel", command=root.destroy).pack()

        root.mainloop()

        if result["value"]:
            return result["value"] + ".html"
        return config.DEFAULT_OUTPUT_FILENAME
