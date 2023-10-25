from pathlib import Path
from os import path, listdir, chdir
from datetime import datetime

class ParentFolder:

    def __init__(self, parent):
        self.parent_directory = parent
    
    @staticmethod
    def fetch_modification_time(file):
        '''Fetches file modification timestamp in Unix format'''
        return path.getmtime(file)
    
    @staticmethod
    def convert_modification_time(timestamp):
        '''Converts Unix timestamp to a readable format'''
        modification_date = datetime.utcfromtimestamp(
            timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        return modification_date

    @staticmethod
    def setup_file_transfer(file):
        '''Setup directory for FTP file transfer'''
        transfer = Path(file)
        chdir(transfer.parent)
        return transfer.name

    def fetch_child_items(self):
        '''Fetches files from parent directory'''
        return [Path(self.parent_directory, file) for 
            file in listdir(self.parent_directory) if not
            Path(self.parent_directory, file).is_dir()]

    def format_file_dates(self, files):
        '''Format the file paths and datetimes into a list of tuples'''
        timestamps = []
        for file in files:
            timestamps.append((str(file), self.fetch_modification_time(file)))
        
        return timestamps
