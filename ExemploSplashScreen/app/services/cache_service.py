
import sqlite3

class CacheService:

    def __init__(self):
        self.conn = sqlite3.connect("cache.db", check_same_thread=False)
        self.conn.execute("CREATE TABLE IF NOT EXISTS cache (hash TEXT PRIMARY KEY, text TEXT)")

    def exists(self, hash_value):
        cur = self.conn.execute("SELECT 1 FROM cache WHERE hash=?", (hash_value,))
        return cur.fetchone() is not None

    def save(self, hash_value, text):
        self.conn.execute("INSERT OR IGNORE INTO cache VALUES (?,?)", (hash_value, text))
        self.conn.commit()
