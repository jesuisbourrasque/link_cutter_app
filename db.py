import sqlite3


class DB:
    def __init__(self):
        self.path_to_db = "db_test.db"
        self.connection = sqlite3.connect(self.path_to_db)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def execute(self, query: str, parameters: tuple = ()):
        cursor = self.cursor
        cursor.execute(query, parameters)

    def fetchone(self):
        data = self.cursor.fetchone()
        return data

    def fetchall(self):
        data = self.cursor.fetchall()
        return data

    def create_schema(self):
        query = """
            CREATE TABLE IF NOT EXISTS long_urls(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL UNIQUE
            )
        """
        self.execute(query)
        query = """
                    CREATE TABLE IF NOT EXISTS short_urls(
                    short_url TEXT NOT NULL UNIQUE,
                    id INTEGER NOT NULL,
                    FOREIGN KEY(id) REFERENCES long_urls(id)
                    )
                """
        self.execute(query)

    def add_long_url(self, long_url):
        query = "INSERT INTO long_urls(long_url) VALUES(?)"
        self.execute(query, (long_url,))

    def lastrowid(self):
        return self.cursor.lastrowid

    def add_short_url(self, short_url):
        query = "INSERT INTO short_urls(short_url, id) VALUES(?, ?)"
        self.execute(query, (short_url, self.lastrowid()))

    def select_long_url(self, short_url):
        """Return long ulr by short url"""
        query = "SELECT id FROM short_urls WHERE short_url = ?"
        self.execute(query, (short_url,))
        long_url_id = self.fetchone()
        query = "SELECT long_url FROM long_urls WHERE id = ?"
        self.execute(query, (long_url_id,))
        return self.fetchone()

