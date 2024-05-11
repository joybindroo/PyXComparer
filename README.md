# PyXComparer
PyXComparer is a Python-based tool designed to simplify the process of monitoring changes between different versions of ODK XLSForms. It provides a user-friendly GUI interface for comparing XLSForm files, helping users to ensure data integrity and consistency in their XLSFom projects.  



## Features

- Compare different versions of XLSForms to identify changes.
- Visualize differences between forms with highlighting and categorization.
- Export comparison results for further analysis or documentation.

## Getting Started

To get started with PyXComparer, follow these steps:

1. Clone the repository to your local machine
2. Navigate to the PyXComparer directory:

**cd PyXComparer**

Install the required dependencies:
**pip install -r requirements.txt**

Run the PyXComparer application:
**python xcomparer.py**

## Usage
- Select the two versions of the XLSForms you want to compare.
- Comparison will be done by first creating YAML files for the forms and then doing a DIFF of the two YAML files.
- The results will be displayed in the GUI, highlighting additions, deletions, and modifications.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## Acknowledgements
PyXComparer was inspired by the need to streamline the process of managing changes between versions of ODK XLSForms when very large surveys are created by many team members and those are merged and improved overtime in limited resource settings. Special thanks to the ODK community for their support and inspiration.
