# Flow Log Parsing Tool

## Overview

This tool processes flow log data and maps each entry to a tag based on a lookup table. It produces an output file containing:

  1. Counts of matches for each tag.

  2. Counts of matches for each port/protocol combination.

## Features:

  - Supports large flow log files (up to 10 MB).

  - Handles up to 10,000 tag mappings.

  - Case-insensitive matching.

  - Identifies and counts untagged flow log entries.

## Input Files

### 1. Flow Logs File

A text file containing flow log entries in the following format:

> 2 123456789012 eni-<instance-id> <source-ip> <destination-ip> <destination-port> <source-port> <protocol> <packets> <bytes> <start-time> <end-time> <action> <log-status>

Example:

> 2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK
> 2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 23 49154 6 15 12000 1620140761 1620140821 REJECT OK

### 2. Lookup Table CSV

A CSV file containing tag mappings with the following structure:

```
dstport,protocol,tag 
25,tcp,sv_P1
68,udp,sv_P2
443,tcp,sv_P2
110,tcp,email
993,tcp,email
```

## Output File

The tool generates an output file containing:

1. Tag Counts Example:

`Tag Counts:
Tag,Count
sv_P1,2
sv_P2,3
email,3
Untagged,5`

2. Port/Protocol Combination Counts Example:

`Port/Protocol Combination Counts:
Port,Protocol,Count
443,tcp,3
25,tcp,2
993,tcp,1`

## How to Use the Tool

### 1. Prepare the Input Files

- flow logs file saved under the path `/home/alo/experimental` with the file name as `flow_log.txt`.
- lookup_table file saved under the path `/home/alo/experimental` with the file name as `lookup_table.csv`.

### 2. Run the Script

Execute the tool using Python:

python flowlog_parser.py

### 3. Review the Output

The results will be written to `output_results.txt` under the path `/home/alo/experimental`.

## Requirements

Python 3.x

## Implementation Details

### Functions

- `load_lookup_table(file_path)`: Loads the lookup table and returns a dictionary of mappings.

- `parse_flow_logs(file_path)`: Parses flow log entries into a usable format.

- `process_logs(flow_logs, lookup_table)`: Maps flow logs to tags and counts occurrences.

- `write_output(output_path, tag_counts, port_protocol_counts)`: Writes results to the output file.

## Error Handling

- Missing Files: If input files are not found, the script will raise a FileNotFoundError.

- Invalid Formats: Logs or lookup tables in incorrect formats will trigger parsing errors.

## Customization

Modify the default file paths in the main() function to use custom input/output locations.

## Example Execution

1. Place the `flow_logs.txt` and `lookup_table.csv` files in the working directory.

2. Run the script:

> python flowlog_parser.py

3. Check the output_results.txt for the parsed results.

## Support

For questions or issues, please contact alo.angellolo@gmail.com.

