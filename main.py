import sys
import shortuuid

from db import DB
from parser import parse_args


def main():
    args = parse_args(sys.argv[1:])
    url = args.url
    generate = args.generate
    short_url = args.short_url
    with DB() as db:
        db.create_schema()
        if generate:
            if not short_url:
                short_url = shortuuid.uuid(url)
            if db.add_url(url, short_url):
                print(f'Короткая ссылка на вашу {short_url}')
            else:
                print(f'Такая короткая ссылка уже существует: {short_url}')
        if not generate and url:
            if long_url := db.select_long_url(url):
                print(long_url)
            else:
                print('Такой ссылки нет')


if __name__ == '__main__':
    main()