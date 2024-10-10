class Database:
    def __init__(self, db_file):
        self.conn = None
        self.db_file = db_file

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            print("Connection established")
        except sqlite3.Error as e:
            print("Error connecting to database:", e)

    def close(self):
        if self.conn:
            self.conn.close()
            print("Connection closed")