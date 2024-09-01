import csv
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

    def parse(self, flow_log_file, lookup_dict,**kwargs):
        pass

    def write(self, tag_count, port_protocol_count, untagged_count,**kwargs):
        pass    

    def run(self, lookup_file, flow_log_file):
        lookup_dict = self.read(lookup_file)
        # print(lookup_dict)


if __name__ == "__main__":
    lookup_file = 'lookup_table.csv'
    flow_log_file = 'flow_logs.txt'
    
    parser = FlowLogParser()
    parser.run(lookup_file, flow_log_file)