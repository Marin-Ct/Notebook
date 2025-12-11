class FileReader:
    @staticmethod
    def read_file_to_string(path):
        """Read the file at the given path and return its contents as a string."""
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
