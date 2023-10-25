from ftplib import FTP
from datetime import datetime
from creds import params

class VirtualDisk:

    def __init__(self):
        '''Initialize Mailo.com VirtualDisk server connection'''
        self.ftp = FTP(host='ftp.mailo.com', 
            user=params['acct_name'], 
            passwd=params['password'],
            encoding='utf-8')
    
    def change_folder_directory(self, directory):
        '''Change FTP server directory'''
        self.ftp.cwd(directory)
    
    @staticmethod
    def format_timestamp(value):
        '''Formats the FTP server timestamp to Year:Month:Day Hour:Minute:Second'''
        return datetime.strptime(value[7:], '%Y%m%d%H%M%S').timestamp()
    
    def server_contents(self, directory_path):
        '''Print server directory contents'''
        contents = []
        self.ftp.retrlines('MLSD', contents.append)
        _filter = [entry.split(';') for entry in contents]
        return [(f'{directory_path}\\{value[-1].strip()}', 
            self.format_timestamp(value[2])) for value in _filter[2:]]
    
    def upload_file(self, file):
        '''Upload file to VirtualDisk server'''
        print(f'Uploading {file} to ftp.mailo.com...')
        with open(file, 'rb') as upload:
            self.ftp.storbinary(f'STOR {file}', upload)
    
    def download_file(self, file):
        '''Download file from VirtualDisk server'''
        with open(file, 'wb') as download:
            self.ftp.retrbinary(f'RETR {file}', download.write)
    
    def close_connection(self):
        '''Close VirtualDisk server conneciton'''
        self.ftp.quit()