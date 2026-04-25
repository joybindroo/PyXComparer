import yaml
import pandas as pd
from pathlib import Path
from pyxcomparer.exceptions import XLSFormError

def convert_xlsform_to_yaml(xlsform_path, output_path=None):
    """
    Converts an XLSForm to a comprehensive YAML representation.
    """
    try:
        path = Path(xlsform_path)
        xls = pd.ExcelFile(path)
        
        # Extract survey and choices sheets
        survey_df = xls.parse('survey')
        choices_df = xls.parse('choices') if 'choices' in xls.sheet_names else pd.DataFrame()

        # Process survey
        survey_data = []
        for _, row in survey_df.iterrows():
            # Filter out rows without a 'type' or 'name' (like section headers)
            if pd.isna(row['type']) or pd.isna(row['name']):
                continue
            
            item = {
                'type': str(row['type']),
                'name': str(row['name']),
                'label': str(row['label']) if not pd.isna(row['label']) else 'N/A',
            }
            
            # Add optional columns if they exist
            for col in ['constraint', 'relevance', 'appearance', 'required']:
                if col in survey_df.columns and not pd.isna(row[col]):
                    item[col] = str(row[col])
            
            survey_data.append(item)

        # Process choices into a dictionary mapping list_name -> list of choices
        choices_data = {}
        if not choices_df.empty:
            # Group by 'list_name'
            grouped = choices_df.groupby('list_name')
            for list_name, group in grouped:
                choices_list = []
                for _, row in group.iterrows():
                    choices_list.append({
                        'name': str(row['name']),
                        'label': str(row['label']) if not pd.isna(row['label']) else 'N/A'
                    })
                choices_data[str(list_name)] = choices_list

        full_metadata = {
            'survey': survey_data,
            'choices': choices_data
        }

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(full_metadata, f, sort_keys=False, allow_unicode=True)
            return Path(output_path)
        
        return full_metadata

    except Exception as e:
        raise XLSFormError(f"Failed to convert XLSForm to YAML: {str(e)}")
