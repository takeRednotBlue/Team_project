from abc import ABC, abstractmethod

class TerminalOutput(ABC):
    @abstractmethod
    def output_table_format(self, headers, data):
        pass

    @abstractmethod
    def output_help_msg(self, headers, data):
        pass