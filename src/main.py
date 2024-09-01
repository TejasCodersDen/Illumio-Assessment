import csv, sys, os, logging
from collections import defaultdict
from AbstractLogParser import AbstractLogParser
from exceptions import FileNotFound, InvalidFileFormat, InvalidLookupTableEntry, FileWritePermissionError

# Set up logging configuration to log errors in the 'log' directory
log_dir = os.path.join(os.path.dirname(__file__), '..', 'log')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, 'flow_log_parser.log'),
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class FlowLogParser(AbstractLogParser):
    """
    FlowLogParser is responsible for reading a lookup table, parsing a flow log file,
    and writing the results to output CSV files. It inherits from AbstractLogParser.
    """

    def read(self, lookup_file):
        """
        Reads the lookup table from a CSV file and returns a dictionary
        mapping (dstport, protocol) to tag.
        """
        lookup_dict = {}
        try:
            with open(lookup_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    if len(row) == 3:
                        dstport, protocol, tag = row
                        lookup_dict[(dstport.strip(), protocol.strip().lower())] = tag.strip()
                    else:
                        logging.error(f"Invalid Lookup Table Entry: {row}")
                        raise InvalidLookupTableEntry(row)
        except FileNotFoundError:
            logging.error(f"File not found: {lookup_file}")
            raise FileNotFound(lookup_file)
        except csv.Error:
            logging.error(f"Invalid file format: {lookup_file}")
            raise InvalidFileFormat(lookup_file)

        return lookup_dict

    def parse(self, flow_log_file, lookup_dict):
        """
        Parses the flow log file and counts occurrences of tags and port/protocol combinations.
        """
        tag_count = defaultdict(int)
        port_protocol_count = defaultdict(int)
        untagged_count = 0

        try:
            with open(flow_log_file, 'r') as file:
                for line in file:
                    parts = line.split()
                    if len(parts) >= 8 and parts[0] == '2':
                        dstport = parts[5]
                        protocol = self._protocol_mapping(parts[7])
                        key = (dstport, protocol)
                        port_protocol_count[key] += 1

                        if key in lookup_dict:
                            tag_count[lookup_dict[key]] += 1
                        else:
                            untagged_count += 1
        except FileNotFoundError:
            logging.error(f"File not found: {flow_log_file}")
            raise FileNotFound(flow_log_file)
        except csv.Error:
            logging.error(f"Invalid file format: {flow_log_file}")
            raise InvalidFileFormat(flow_log_file)
        
        return tag_count, port_protocol_count, untagged_count
    
    def _protocol_mapping(self, protocol_number):
        """
        Maps protocol numbers from the flow log to protocol names used in the lookup table.
        """
        protocol_map = {
            '6' : 'tcp',
            '17' : 'udp'
        }

        return protocol_map.get(protocol_number, 'unmapped')

    def write(self, tag_count, port_protocol_count, untagged_count, tag_counts_file, port_protocol_counts_file):
        """
        Writes the tag counts and port/protocol counts to CSV files.
        """
        try:
            with open(tag_counts_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Tag", "Count"])
                for tag, count in tag_count.items():
                    writer.writerow([tag, count])
                writer.writerow(["Untagged", untagged_count])

            with open(port_protocol_counts_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Port", "Protocol", "Count"])
                for (port, protocol), count in port_protocol_count.items():
                    writer.writerow([port, protocol, count])
        except PermissionError as e:
            logging.error(f"Permission denied: {e}")
            raise FileWritePermissionError(f"Permission denied: {e}")

    def run(self, lookup_file, flow_log_file, tag_counts_file, port_protocol_counts_file):
        """
        Executes the full parsing process: reads the lookup table, parses the flow log,
        and writes the results to output files.
        """
        lookup_dict = self.read(lookup_file)
        tag_count, port_protocol_count, untagged_count = self.parse(flow_log_file, lookup_dict)
        self.write(tag_count, port_protocol_count, untagged_count, tag_counts_file, port_protocol_counts_file)


if __name__ == "__main__":

    # Define the directories for data input and output
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    
    # Define default file paths
    lookup_file = os.path.join(data_dir, 'lookup_table.csv')
    flow_log_file = os.path.join(data_dir, 'flow_logs.txt')
    tag_counts_file = os.path.join(output_dir, 'tag_counts.csv')
    port_protocol_counts_file = os.path.join(output_dir, 'port_protocol_counts.csv')
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Handle command-line arguments
    if len(sys.argv) == 3:
        lookup_file = sys.argv[1]
        flow_log_file = sys.argv[2]
    elif len(sys.argv) > 1:
        print("Error: Please provide both the lookup file and the flow log file paths, or provide none to use default paths.")
        sys.exit(1)
    
    parser = FlowLogParser()
    parser.run(lookup_file, flow_log_file, tag_counts_file, port_protocol_counts_file)
