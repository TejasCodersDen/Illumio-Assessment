from abc import ABC, abstractmethod

class AbstractLogParser(ABC):
    @abstractmethod
    def read(self, lookup_file, **kwargs):
        pass

    @abstractmethod
    def parse(self, flow_log_file, lookup_dict, **kwargs):
        pass

    @abstractmethod
    def write(self, tag_count, port_protocol_count, untagged_count, **kwargs):
        pass

    @abstractmethod 
    def run(self, lookup_file, flow_log_file, **kwargs):
        pass
