import csv
from collections import defaultdict

def load_lookup_table(file_path):
    """Loads the lookup table from a CSV file."""
    lookup_table = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            port = row['dstport'].strip()
            protocol = row['protocol'].strip().lower()
            tag = row['tag'].strip()
            lookup_table[(port, protocol)] = tag
    return lookup_table

def parse_flow_logs(file_path):
    """Parses the flow logs from the input file."""
    flow_logs = []
    with open(file_path, 'r') as file:
        for line in file:
            fields = line.strip().split()
            if len(fields) >= 14:
                dst_port = fields[5]
                protocol = 'tcp' if fields[7] == '6' else 'udp' if fields[7] == '17' else 'icmp'
                flow_logs.append((dst_port, protocol))
    return flow_logs

def process_logs(flow_logs, lookup_table):
    """Processes the flow logs and matches them with the lookup table."""
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)

    for dst_port, protocol in flow_logs:
        tag = lookup_table.get((dst_port, protocol), "Untagged")
        tag_counts[tag] += 1
        port_protocol_counts[(dst_port, protocol)] += 1

    return tag_counts, port_protocol_counts

def write_output(output_path, tag_counts, port_protocol_counts):
    """Writes the processed data to an output file."""
    with open(output_path, 'w') as outfile:
        # Write tag counts
        outfile.write("Tag Counts:\n")
        outfile.write("Tag,Count\n")
        for tag, count in sorted(tag_counts.items()):
            outfile.write(f"{tag},{count}\n")

        outfile.write("\nPort/Protocol Combination Counts:\n")
        outfile.write("Port,Protocol,Count\n")
        for (port, protocol), count in sorted(port_protocol_counts.items()):
            outfile.write(f"{port},{protocol},{count}\n")

def main():
    lookup_file = "/home/alo/experimental/lookup_table.csv"  # Path to lookup table CSV
    flow_logs_file = "/home/alo/experimental/flow_log_data.txt"  # Path to flow logs file
    output_file = "/home/alo/experimental/output_results.txt"  # Path to output file

    lookup_table = load_lookup_table(lookup_file)
    flow_logs = parse_flow_logs(flow_logs_file)
    tag_counts, port_protocol_counts = process_logs(flow_logs, lookup_table)
    write_output(output_file, tag_counts, port_protocol_counts)

if __name__ == "__main__":
    main()