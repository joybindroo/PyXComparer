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

## Human-Readable Data Dictionary or Metadata
PyXComparer not only helps in comparing different versions of ODK XLSForms but also facilitates the generation of a human-readable data dictionary or metadata. By parsing and analyzing the structure of the XLSForm files, PyXComparer extracts information such as questions, choices, and settings like data validation and whehter question is mandatory or not. This information is then organized and presented in a clear and concise format, making it easily understandable for teams working on data collection and analysis.

The generated data dictionary provides detailed descriptions of each field, including the question text, data type, constraints, and relevant notes. Additionally, it highlights any changes or updates made between different versions of the XLSForms, ensuring that teams are aware of any modifications and can adapt their data collection and analysis processes accordingly.

With this human-readable YAML syntax metadata, teams can quickly grasp the structure and requirements of the data collection forms, facilitating efficient communication and collaboration. It serves as a valuable reference for data collectors, analysts, and stakeholders, helping them better understand the dataset and make informed decisions based on the collected data.


## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.



## Acknowledgements
PyXComparer was inspired by the need to streamline the process of managing changes between versions of ODK XLSForms when very large surveys are created by many team members and those are merged and improved overtime in limited resource settings. Special thanks to the ODK community for their support and inspiration.
