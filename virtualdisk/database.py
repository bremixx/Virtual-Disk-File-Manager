import sqlite3

class Database:
    '''Sets up local file database and handles timestamp checking with FTP server'''

    def __init__(self):
        '''Create SQL database for timestamp storage'''
        self.con = sqlite3.connect('timestamp.db')
        
        self.cur = self.con.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS ts(
                    path, timestamp)''')

        self.con.commit()

        self.files_to_upload = []
    
    def add_to_db(self, records):
        '''Add modified files to SQL database'''
        print(f'Adding {records[0]} to database...')
        self.files_to_upload.append(records[0])
        self.cur.executemany('INSERT INTO ts VALUES (?, ?)', (records, ))
        self.con.commit()
    
    def query_db(self):
        '''Search database for matching file modification timestamp'''
        self.cur.execute('SELECT * FROM ts')
        return self.cur.fetchall()

    def update_db(self, local):
        '''Sends file updated timestamp to SQL database'''
        print(f'{local[0]} timestamp is out of date...')
        self.cur.execute('''UPDATE ts SET timestamp = ? 
            WHERE path = ?''', (local[1], local[0]))
        self.con.commit()

    def delete_entry(self, entry):
        '''Delete record from SQL database'''
        print(f'Deleting {entry[0]} from database...')
        self.cur.execute('DELETE FROM ts WHERE path = ?', (entry[0], ))
        self.con.commit()

    @staticmethod
    def comparison(values, ref, func):
        '''Generic function to compare local files to database'''
        for file in values:
            if file not in ref:
                func(file)

    def compare_local_db(self, files):
        '''Compare local files to database'''

        self.comparison(values=files, ref=self.query_db(), 
            func=self.add_to_db)
        self.comparison(values=self.query_db(), 
            ref=files, func=self.delete_entry)

        for local, db in zip(sorted(files), sorted(self.query_db())):
            if local != db: 
                self.files_to_upload.append(local[0])
                self.update_db(local)
        
        return self.files_to_upload

    def close_db(self):
        '''Close SQL database connection'''
        self.con.close()
    
    def compare_db_server(self, database, virtualdisk):
        '''Compare SQL database files to FTP server'''
        for db, server in zip(sorted(database), sorted(virtualdisk)):
            if db[0] in server[0]:
                if db[1] > server[1]: self.files_to_upload.append(db[0])
            else: self.files_to_upload.append(db[0])
        
        return self.files_to_upload