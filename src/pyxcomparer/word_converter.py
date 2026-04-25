import pandas as pd
from pathlib import Path

def convert_yaml_to_word(metadata, output_path="specification.docx"):
    """
    Converts ODK YAML metadata to a professional Word document specification.
    
    Args:
        metadata (dict): The full metadata dictionary containing 'survey' and 'choices'.
        output_path (str): Path to save the .docx file.
    """
    from docx import Document
    from docx.shared import Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    doc = Document()
    
    # Title
    title = doc.add_heading('ODK Form Technical Specification', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Extract sections
    survey = metadata.get('survey', [])
    choices = metadata.get('choices', {})

    if not survey:
        print("No survey data found in metadata.")
        return Path(output_path)

    # Table for survey questions
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Table Grid'
    
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Field Name'
    hdr_cells[1].text = 'Label'
    hdr_cells[2].text = 'Type'
    hdr_cells[3].text = 'Details/Options'

    for item in survey:
        row_cells = table.add_row().cells
        
        # Basic info
        name = item.get('name', 'N/A')
        label = item.get('label', 'N/A')
        q_type = item.get('type', 'N/A')
        
        row_cells[0].text = str(name)
        row_cells[1].text = str(label)
        row_cells[2].text = str(q_type)
        
        # Handle Choices for select_one and select_multiple
        details = []
        if isinstance(q_type, str) and (q_type.startswith('select_one') or q_type.startswith('select_multiple')):
            # Extract choice list name from type (e.g., 'select_one gender' -> 'gender')
            parts = q_type.split(' ')
            if len(parts) > 1:
                choice_list_name = parts[1]
                choice_data = choices.get(choice_list_name, [])
                
                if choice_data:
                    options = [f"{c.get('name')}: {c.get('label')}" for c in choice_data]
                    details.append("Options:\n" + "\n".join(options))
                else:
                    details.append("Choice list not found in metadata.")
        
        # Add other details like constraints or relevance if they exist
        if 'constraint' in item:
            details.append(f"Constraint: {item['constraint']}")
        if 'relevance' in item:
            details.append(f"Relevance: {item['relevance']}")

        row_cells[3].text = "\n".join(details) if details else "N/A"

    doc.save(output_path)
    return Path(output_path)
