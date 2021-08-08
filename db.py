import sqlite3
from typing import Optional


class DB:
    def __init__(self):
        self.connection = sqlite3.connect('main_db.db')
        self.cursor = self.connection.cursor()

    def __enter__(self) -> 'DB':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.connection.commit()
        self.connection.close()

    def create_schema(self) -> None:
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

    def add_url(self, long_url: str, short_url: str) -> bool:
        """
        :param long_url: url by user input
        :param short_url: url by user input or generated
        :return:
        """
        query = """
            SELECT long_urls.id 
            FROM long_urls 
            WHERE long_urls.long_url = ?
        """
        long_url_id = self.cursor.execute(query, (long_url,))
        if long_url_id := long_url_id.fetchone():
            return self.add_short_url(short_url, long_url_id[0])

        query = """
            INSERT INTO long_urls(long_url) 
            VALUES (?)
        """
        self.cursor.execute(query, (long_url,))
        return self.add_short_url(short_url, self.cursor.lastrowid)

    def add_short_url(self, short_url: str, long_url_id: int) -> bool:
        """
        :param short_url: url by user input or generated
        :param long_url_id: id of long_url in the long_urls table
        :return: if short_url exists -> False else -> True
        """
        query = """
            SELECT short_url 
            FROM short_urls 
            WHERE short_urls = ?
        """
        is_short_url = self.cursor.execute(query, (short_url,))
        if is_short_url.fetchone():
            return False

        query = """
            INSERT INTO short_urls(short_url, id) 
            VALUES(?, ?)
        """
        self.cursor.execute(query, (short_url, long_url_id))
        return True

    def select_long_url(self, short_url: str) -> Optional[str]:
        """
        Select long url in the long_urls table by short_url
        :param short_url: url by user input or generated
        :return: Long url if exists or None
        """
        query = """
            SELECT long_url 
            FROM long_urls 
            JOIN short_urls 
                ON long_urls.id = short_urls.id 
            WHERE short_url = ?
        """
        self.cursor.execute(query, (short_url,))
        if long_url := self.cursor.fetchone():
            return long_url[0]
