import sqlite3


class DB:
    def __init__(self):
        self.path_to_db = "/db.db"

    @property
    def connection(self):
        """Return connection to db"""
        connection = sqlite3.connect(self.path_to_db)
        connection.row_factory = sqlite3.Row
        return connection

    def execute(self, query: str, connection, parameters: tuple = (), fetchone=False, fetchall=False, commit=False):
        cursor = connection.cursor()
        try:
            cursor.execute(query, parameters)
            data = None
            if commit:
                connection.commit()
            if fetchone:
                data = cursor.fetchone()
            elif fetchall:
                data = [dict(row) for row in cursor.fetchall()]
            return data
        finally:
            connection.close()

    def create_long_urls_schema(self):
        query = """
            CREATE TABLE IF NOT EXISTS long_urls(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL UNIQUE,
            )
        """
        self.execute(query, self.connection, commit=True)

    def create_short_urls_chema(self):
        query = """
            CREATE TABLE IF NOT EXISTS short_urls(
            short_url TEXT NOT NULL UNIQUE,
            id INTEGER NOT NULL
            FOREIGN KEY(id) REFERENCES long_urls(id)
            )
        """
        self.execute(query, self.connection, commit=True)

    def add_urls(self, url):
        query = "INSERT INTO long_url(long_url) VALUES(?)"
        self.execute(query, self.connection, url, commit=True)
