from argparse import ArgumentParser
from parent import ParentFolder
from virtualdisk import VirtualDisk
from database import Database

def main():

    parser = ArgumentParser(prog='Virtual disk updater',
    description='Automatically sends files to a mailo(dot)com Virtual Disk server.')

    parser.add_argument('directory')
    args = parser.parse_args()

    pf = ParentFolder(args.directory)
    files = pf.fetch_child_items()
    timestamped = pf.format_file_dates(files)
    db = Database()
    db.compare_local_db(timestamped)
    try:
        vd = VirtualDisk()
        vd.change_folder_directory('My Notes')
        files_to_upload = db.compare_db_server(db.query_db(), 
            vd.server_contents(directory_path=args.directory))
        for file in files_to_upload:
            vd.upload_file(pf.setup_file_transfer(file))
    finally:
        print('File transfer complete.')
        vd.close_connection()