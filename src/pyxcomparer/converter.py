import yaml
import pandas as pd
from pathlib import Path
from pyxcomparer.exceptions import XLSFormError
from pyxcomparer.config import config

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

            # Handle multi-language labels (e.g., label::English, label::Hindi)
            # We prefer English if available, otherwise take the first label column
            label = 'N/A'
            label_cols = [col for col in survey_df.columns if col.startswith('label')]
            if label_cols:
                # Try to find English label first
                eng_col = next((col for col in label_cols if 'English' in col), None)
                if eng_col and not pd.isna(row[eng_col]):
                    label = str(row[eng_col])
                elif not pd.isna(row[label_cols[0]]):
                    label = str(row[label_cols[0]])

            item = {
                'type': str(row['type']),
                'name': str(row['name']),
                'label': label,
            }

            # Add optional columns if they exist
            for col in ['constraint', 'relevance', 'appearance', 'required']:
                # Check for multi-language versions of these columns too
                actual_col = next((c for c in survey_df.columns if c.startswith(col)), None)
                if actual_col and not pd.isna(row[actual_col]):
                    item[col] = str(row[actual_col])

            survey_data.append(item)

        # Process choices into a dictionary mapping list_name -> list of choices
        choices_data = {}
        if not choices_df.empty:
            # Group by 'list_name'
            grouped = choices_df.groupby('list_name')
            for list_name, group in grouped:
                choices_list = []
                for _, row in group.iterrows():
                    # Handle multi-language labels for choices
                    label = 'N/A'
                    label_cols = [col for col in choices_df.columns if col.startswith('label')]
                    if label_cols:
                        eng_col = next((col for col in label_cols if 'English' in col), None)
                        if eng_col and not pd.isna(row[eng_col]):
                            label = str(row[eng_col])
                        elif not pd.isna(row[label_cols[0]]):
                            label = str(row[label_cols[0]])

                    choices_list.append({
                        'name': str(row['name']),
                        'label': label
                    })

                # Apply choice limit from config
                limit = config.MAX_CHOICES_DISPLAY
                if limit and limit > 0 and len(choices_list) > limit:
                    choices_list = choices_list[:limit]
                    # Add a special entry to indicate truncation
                    choices_list.append({'name': 'truncated', 'label': f"... ({len(group) - limit} more options omitted)"})

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
