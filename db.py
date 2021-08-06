import sqlite3


class DB:
    def __init__(self):
        self.path_to_db = "db.db"

    @property
    def connection(self):
        """Return connection to db"""
        connection = sqlite3.connect(self.path_to_db)
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
                data = cursor.fetchall()
            return data
        finally:
            connection.close()

    def create_long_urls_schema(self):
        query = """
            CREATE TABLE IF NOT EXISTS long_urls(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL UNIQUE
            )
        """
        self.execute(query, self.connection, commit=True)

    def create_short_urls_chema(self):
        query = """
            CREATE TABLE IF NOT EXISTS short_urls(
            short_url TEXT NOT NULL UNIQUE,
            id INTEGER NOT NULL,
            FOREIGN KEY(id) REFERENCES long_urls(id)
            )
        """
        self.execute(query, self.connection, commit=True)

    def add_long_url(self, long_url):
        query = "INSERT INTO long_urls(long_url) VALUES(?)"
        self.execute(query, self.connection, (long_url,), commit=True)

    def add_short_url(self, long_url, short_url):
        query = "SELECT id FROM long_urls WHERE long_url = ?"
        long_url_id = self.execute(query, self.connection, (long_url,), fetchone=True)
        query = "INSERT INTO short_urls(short_url, id) VALUES(?, ?)"
        self.execute(query, self.connection, (short_url, long_url_id[0]), commit=True)

    def select_long_url(self, short_url):
        """Return long ulr by short url"""
        query = "SELECT id FROM short_urls WHERE short_url = ?"
        long_url_id = self.execute(query, self.connection, (short_url,), fetchone=True)
        query = "SELECT long_url FROM long_urls WHERE id = ?"
        return self.execute(query, self.connection, (long_url_id[0],), fetchone=True)[0]

