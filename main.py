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
                database.add_long_url(url)
            except Exception:
                pass
            if short_url:
                try:
                    database.add_short_url(short_url)
                    print(f'Короткая ссылка на вашу {short_url}')
                except Exception:
                    print(f'Такая короткая ссылка уже существует: {short_url}')
            elif not short_url:
                try:
                    short_url = shortuuid.uuid(url)
                    database.add_short_url(short_url)
                    print(f'Короткая ссылка на вашу {short_url}')
                except Exception as e:
                    print(e)
        if not generate and url:
            long_url = database.select_long_url(url)
            if long_url:
                print(long_url)
            else:
                print('Такой ссылки нет')


if __name__ == '__main__':
    main()