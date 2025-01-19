# User Manual

## SAE1.05 Project - Network Data Analysis

### Description

This project involves analyzing network data from a text file (e.g., a tcpdump file). The script extracts relevant information such as IP addresses, flags, sequences, and payloads. It generates CSV files, creates visualizations, and produces an HTML report. The generated CSV files can also be imported into Excel for further analysis.

### Requirements

- **Python 3.13.1**: Ensure Python is installed on your system.
- **Python Libraries**: The script requires the following libraries:
  - `csv`
  - `matplotlib`
  - `os`
  - `tempfile`
  - `shutil`
  - `markdown`
  - `webbrowser`
  - `openpyxl`

To install the required libraries, run the following command:
```bash
pip install matplotlib markdown openpyxl
```

### Usage

1. **Prepare the Input File**

   Place the network capture file (e.g., `DumpFile.txt`) in the project directory or specify its path when running the script.

2. **Run the Script**

   Open a terminal or command prompt.

   Navigate to the directory containing the script (`SAE105.py`).

   Run the script using the following command:
   ```bash
   python SAE105.py
   ```

3. **Load a File**

   A graphical interface will open. Click the "Load a File" button to select the network capture file for analysis.

4. **Generated Results**

   After the analysis, the following files will be generated:
   - **HTML Report**: A report containing a summary of detected issues and a bar chart.
   - **CSV File**: A file containing the detected issues in a structured format.
   - **Markdown File**: A Markdown version of the report for easy sharing and documentation.

### Using the Generated Files

1. **HTML Report**

   The HTML report contains:
   - A summary table of detected issues.
   - A bar chart showing the distribution of issues.

   To view the report, click the "Open in Browser" button in the application.

2. **CSV File**

   The CSV file contains the detected issues with the following columns:
   - **Type**: The type of issue (DNS Error, Suspicious SYN, Repetition).
   - **Description**: A description of the issue.
   - **Frame**: The content of the suspicious packet.

   To save the CSV file, click the "Save as CSV" button in the application. You can open this file in Excel for further analysis.

3. **Markdown File**

   The Markdown file contains the detected issues in a structured format, suitable for documentation or sharing.

   To save the Markdown file, click the "Save as Markdown" button in the application.

### Interpreting the Results

1. **HTML Report**

   The HTML report provides a quick overview of the detected issues and their distribution.

   Use the bar chart to identify the most common issues (e.g., DNS errors, suspicious SYN packets).

2. **CSV File**

   The CSV file contains detailed information about each issue.

   You can use Excel to filter, sort, or analyze the data further.

3. **Markdown File**

   The Markdown file is useful for documentation or sharing the results in a text-based format.

### Example Commands

- **Run the Script**:
  ```bash
  python SAE105.py
  ```

- **Load a File**:
  Click the "Load a File" button and select `DumpFile.txt`.

- **View the Results**:
  - Click "Open in Browser" to view the HTML report.
  - Click "Save as CSV" to save the results in CSV format.
  - Click "Save as Markdown" to save the results in Markdown format.