"""Flask web interface for PyXComparer."""

import os
from pathlib import Path
from flask import Flask, render_template, request, send_file, redirect, url_for, flash

from pyxcomparer.converter import convert_xlsform_to_yaml
from pyxcomparer.comparator import get_diff_summary
from pyxcomparer.reporter import generate_html_report
from pyxcomparer.word_converter import convert_yaml_to_word
from pyxcomparer.exceptions import XLSFormError


app = Flask(__name__, 
            template_folder='templates', 
            static_folder='static')
app.secret_key = os.environ.get("SECRET_KEY", "pyxcomparer-secret-key")

# Setup upload and output directories
UPLOAD_FOLDER = Path("uploads")
OUTPUT_FOLDER = Path("reports")
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    """Main page for uploading and comparing XLSForms."""
    if request.method == "POST":
        # Handle file uploads
        if "file1" not in request.files or "file2" not in request.files:
            flash("Please upload both XLSForm files.")
            return redirect(url_for("index"))

        f1 = request.files["file1"]
        f2 = request.files["file2"]

        if f1.filename == "" or f2.filename == "":
            flash("Please select valid files.")
            return redirect(url_for("index"))

        try:
            # Save uploaded files
            path1 = UPLOAD_FOLDER / f1.filename
            path2 = UPLOAD_FOLDER / f2.filename
            f1.save(path1)
            f2.save(path2)

            # Process: Convert -> Compare -> Report
            yaml1 = convert_xlsform_to_yaml(path1, output_dir=UPLOAD_FOLDER)
            yaml2 = convert_xlsform_to_yaml(path2, output_dir=UPLOAD_FOLDER)
            
            summary = get_diff_summary(yaml1, yaml2)
            
            # Generate HTML report
            report_path = generate_html_report(
                yaml1, yaml2,
                output_path=OUTPUT_FOLDER / f"report_{f1.filename}_{f2.filename}.html"
            )

            # Generate Word Specification for the NEWER form only
            word2_path = convert_yaml_to_word(yaml2, output_path=OUTPUT_FOLDER / f"spec_{f2.filename}.docx")

            return render_template(
                "result.html",
                summary=summary,
                report_url=url_for("download_report", filename=report_path.name),
                word_url=url_for("download_report", filename=word2_path.name)
            )



        except XLSFormError as e:
            flash(f"XLSForm Error: {str(e)}")
        except Exception as e:
            flash(f"Unexpected Error: {str(e)}")
        
        return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/download/<filename>")
def download_report(filename):
    """Serve the generated HTML report."""
    return send_file(OUTPUT_FOLDER / filename)

if __name__ == "__main__":
    # Use environment variables for host/port to support Docker
    app.run(
        host=os.environ.get("FLASK_HOST", "0.0.0.0"),
        port=int(os.environ.get("FLASK_PORT", 5000)),
        debug=os.environ.get("FLASK_DEBUG", "False") == "True"
    )
