import sqlite3


class DB:
    def __init__(self):
        self.path_to_db = "db.db"
        self.connection = sqlite3.connect(self.path_to_db)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()

    def execute(self, query: str, parameters: tuple = ()):
        self.cursor.execute(query, parameters)

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
        return self.cursor.lastrowid

    def add_short_url(self, short_url, id):
        query = "INSERT INTO short_urls(short_url, id) VALUES(?, ?)"
        self.execute(query, (short_url, id))

    def select_long_url(self, short_url):
        """Return long ulr by short url"""
        query = """
            SELECT long_url 
            FROM long_urls 
            JOIN short_urls 
                ON long_urls.id = short_urls.id 
            WHERE short_url = ?
        """
        self.execute(query, (short_url,))
        return self.cursor.fetchone()[0]

    def select_all(self):
        query = "SELECT * FROM long_urls"
        self.execute(query)
        return self.cursor.fetchall()

