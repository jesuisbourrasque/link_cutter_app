import sqlite3
import sys
import shortuuid

from db import DB
from parser import parse_args

database = DB()


def main():
    args = parse_args(sys.argv[1:])
    url = args.url
    generate = args.generate
    short_url = args.short_url
    with database as db:
        db.create_schema()
        if generate:
            try:
                long_url_id = database.add_long_url(url)
            except sqlite3.IntegrityError:
                pass
            try:
                if short_url:
                    pass
                elif not short_url:
                    short_url = shortuuid.uuid(url)
                database.add_short_url(short_url, long_url_id)
            except sqlite3.IntegrityError:
                print(f'Такая короткая ссылка уже существует: {short_url}')
            else:
                print(f'Короткая ссылка на вашу {short_url}')
        if not generate and url:
            try:
                long_url = database.select_long_url(url)
            except TypeError:
                print('Такой ссылки нет')
            else:
                print(long_url)



if __name__ == '__main__':
    main()