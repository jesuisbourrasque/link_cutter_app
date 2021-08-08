import sqlite3


class DB:
    def __enter__(self):
        self.connection = sqlite3.connect("main_db.db")
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()

    def create_schema(self):
        query = """
            CREATE TABLE IF NOT EXISTS long_urls(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL UNIQUE
            )
        """
        self.cursor.execute(query)
        query = """
            CREATE TABLE IF NOT EXISTS short_urls(
            short_url TEXT NOT NULL UNIQUE,
            id INTEGER NOT NULL,
            FOREIGN KEY(id) REFERENCES long_urls(id)
            )
        """
        self.cursor.execute(query)

    def add_url(self, long_url, short_url):
        query = "SELECT long_urls.id FROM long_urls WHERE long_urls.long_url = ?"
        long_url_id = self.cursor.execute(query, (long_url,))
        if long_url_id := long_url_id.fetchone():
            long_url_id = long_url_id[0]
        else:
            query = "INSERT INTO long_urls(long_url) VALUES (?)"
            self.cursor.execute(query, (long_url,))
            long_url_id = self.cursor.lastrowid
        query = "INSERT INTO short_urls(short_url, id) VALUES(?, ?)"
        self.cursor.execute(query, (short_url, long_url_id,))

    def select_long_url(self, short_url):
        """Return long ulr by short url"""
        query = """
            SELECT long_url 
            FROM long_urls 
            JOIN short_urls 
                ON long_urls.id = short_urls.id 
            WHERE short_url = ?
        """
        self.cursor.execute(query, (short_url,))
        if long_url := self.cursor.fetchone()[0]:
            return long_url

