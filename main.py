import csv
import logging
from collections import defaultdict
from AbstractLogParser import AbstractLogParser
from exceptions import FileNotFound, InvalidFileFormat, InvalidLookupTableEntry, FileWritePermissionError

logging.basicConfig(
    filename='flow_log_parser.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class FlowLogParser(AbstractLogParser):
    def read(self, lookup_file):
        lookup_dict = {}
        try:
            with open(lookup_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if len(row) == 3:
                        dstport, protocol, tag = row
                        lookup_dict[(dstport.strip(), protocol.strip().lower())] = tag.strip().lower()
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
        tag_count = defaultdict(int)
        port_protocol_count = defaultdict(int)
        untagged_count = 0

        try:
            with open(flow_log_file, 'r') as file:
                for line in file:
                    parts = line.split()
                    if len(parts) >= 8 and parts[0] == '2':
                        dstport = parts[5]
                        protocol = "tcp" if parts[7] == "6" else "udp"
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

    def write(self, tag_count, port_protocol_count, untagged_count):
        try:
            with open('tag_counts.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Tag", "Count"])
                for tag, count in tag_count.items():
                    writer.writerow([tag, count])
                writer.writerow(["Untagged", untagged_count])

            with open('port_protocol_counts.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Port", "Protocol", "Count"])
                for (port, protocol), count in port_protocol_count.items():
                    writer.writerow([port, protocol, count])
        except PermissionError as e:
            logging.error(f"Permission denied: {e}")
            raise FileWritePermissionError(f"Permission denied: {e}")

    def run(self, lookup_file, flow_log_file):
        lookup_dict = self.read(lookup_file)
        tag_count, port_protocol_count, untagged_count = self.parse(flow_log_file, lookup_dict)
        self.write(tag_count, port_protocol_count, untagged_count)


if __name__ == "__main__":
    lookup_file = 'lookup_table.csv'
    flow_log_file = 'flow_logs.txt'
    
    parser = FlowLogParser()
    parser.run(lookup_file, flow_log_file)