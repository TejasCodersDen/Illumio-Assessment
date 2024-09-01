# Illumio Assessment - Flow Log Parsing Program

## Introduction

The Flow Log Parsing Program is a Python-based application designed to analyze and categorize network flow logs. It reads a flow log file, maps specific port and protocol combinations to predefined tags using a lookup table, and generates detailed output reports in CSV format.

## Assumptions and Limitations

1. **Supported Log Format:** 
   - The program is tailored to support the default flow log format version 2.
   - Custom log formats are not supported.
   
2. **Protocol Identification:** 
   - The tool maps protocol numbers (e.g., 6 for TCP, 17 for UDP) to their respective names as specified in the lookup table.
   - Any unrecognized protocol numbers are categorized as "unknown".
   
3. **Case Insensitivity:** 
   - The matching of protocols in the lookup table and flow log is case insensitive.
   
4. **Handling Unmatched Entries:** 
   - Flow log entries that do not match any tag in the lookup table are classified as "Untagged."

5. **Output Files:** 
   - The program generates two CSV files: one for tag counts and another for port/protocol combination counts.

## Project Structure

- **src/**: Contains the main Python script and supporting modules.
  - `main.py`: The primary script to execute the flow log parsing program.
  - `AbstractLogParser.py`: Defines the abstract base class for the parser.
  - `exceptions.py`: Contains custom exception classes for error handling.

- **data/**: Stores the input files required by the script.
  - `flow_logs.txt`: A sample flow log file.
  - `lookup_table.csv`: The lookup table mapping ports and protocols to tags.

- **output/**: The directory where output files are generated.
  - `tag_counts.csv`: Contains counts of occurrences for each tag.
  - `port_protocol_counts.csv`: Contains counts of occurrences for each port/protocol combination.

- **log/**: Stores log files generated during execution.
  - `flow_log_parser.log`: Log file capturing errors and significant events.

## How to Compile/Run the Program

### Prerequisites

- **Python 3.x**: Ensure that Python 3.x is installed on your local machine.

### Running the Program

1. **Prepare the Files:**
   - Ensure that:
     - `flow_logs.txt` and `lookup_table.csv` are in `data/`
     - maintain rest of the folder structure as is

2. **Execution:**
   - Open a terminal and navigate to the `src` directory:
     ```bash
     cd src
     ```
   - Run the script using Python:
     ```bash
     python3 main.py
     ```

### Command-Line Arguments

- The program supports custom input paths via command-line arguments:
  ```bash
  python main.py /path/to/lookup_table.csv /path/to/flow_logs.txt
  ```
- If no arguments are provided, the script uses the default paths in the `data` directory.

## Output Files

Upon execution, the program generates two output files in the `output` directory:

1. **Tag Counts (`tag_counts.csv`):**
   - Lists the count of flow log entries assigned to each tag.

2. **Port/Protocol Counts (`port_protocol_counts.csv`):**
   - Contains detailed statistics on the occurrence of each port/protocol combination found in the logs.

## Testing and Validation

### Sample Data

- The provided `flow_logs.txt` and `lookup_table.csv` files are sample input files that demonstrate the program's functionality.

### Tested Scenarios

- **Tagging Accuracy:** Verified that flow logs are accurately matched against the lookup table and categorized by tag.
- **Handling Edge Cases:** Ensured that unmatched entries are correctly categorized as "Untagged."
- **Case Insensitivity:** Confirmed that protocol matching is case insensitive.
- **Unknown Protocol Handling:** Verified that any unrecognized protocol numbers are categorized under "unknown."

## Analysis and Considerations

- **Performance:** The script is designed to efficiently process flow logs of moderate size (up to 10 MB), as specified. The line-by-line processing approach ensures minimal memory usage.
- **Scalability:** While the current implementation is optimal for small to medium-sized logs, processing significantly larger datasets may require further optimization or the adoption of more sophisticated parsing strategies.
- **Unit Testing**: Implement comprehensive unit tests for each function within the codebase to validate its functionality, ensure accuracy, and maintain robustness.

## Conclusion

The Flow Log Parsing Program effectively processes flow logs and generates detailed reports, fulfilling the specified requirements. Its simplicity ensures ease of use, with minimal dependencies, making it ideal for quick analysis on local machines.
