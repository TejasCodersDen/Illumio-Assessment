import csv
from collections import defaultdict
from AbstractLogParser import AbstractLogParser

class FlowLogParser(AbstractLogParser):
    def read(self, lookup_file):
        lookup_dict = {}
        with open(lookup_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row) == 3:
                    dstport, protocol, tag = row
                    lookup_dict[(dstport.strip(), protocol.strip().lower())] = tag.strip().lower()

        return lookup_dict

    def parse(self, flow_log_file, lookup_dict):
        tag_count = defaultdict(int)
        port_protocol_count = defaultdict(int)
        untagged_count = 0

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
        
        return tag_count, port_protocol_count, untagged_count

    def write(self, tag_count, port_protocol_count, untagged_count,**kwargs):
        pass    

    def run(self, lookup_file, flow_log_file):
        lookup_dict = self.read(lookup_file)
        tag_count, port_protocol_count, untagged_count = self.parse(flow_log_file, lookup_dict)
        # print(lookup_dict)
        # print(tag_count, port_protocol_count, untagged_count)


if __name__ == "__main__":
    lookup_file = 'lookup_table.csv'
    flow_log_file = 'flow_logs.txt'
    
    parser = FlowLogParser()
    parser.run(lookup_file, flow_log_file)