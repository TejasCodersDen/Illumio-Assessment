class FileNotFound(Exception):
    """Exception raised when a file is not found."""
    def __init__(self, filename):
        self.message = f"File Not Found: {filename}"
        super().__init__(self.message)


class InvalidFileFormat(Exception):
    """Exception raised for errors in the input file format."""
    def __init__(self, filename):
        self.message = f"Invalid File Format: {filename}"
        super().__init__(self.message)


class InvalidLookupTableEntry(Exception):
    """Exception raised when a lookup table entry is invalid."""
    def __init__(self, entry):
        self.message = f"Invalid Lookup Table Entry: {entry}"
        super().__init__(self.message)

class FileWritePermissionError(PermissionError):
    def __init__(self, message="Permission denied: unable to write to the specified file or directory"):
        self.message = message
        super().__init__(self.message)
