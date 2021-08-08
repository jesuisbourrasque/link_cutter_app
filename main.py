import sys

import shortuuid

from db import DB
from parser import parse_args


def main():
    """
    if the user uses the --generate argument
        if the user uses the --short_urls argument with parameter short_url
            try to add data to the database
        else the user don't use --short_urls argument
            generate a short_url and try add to the database
    else the user input short_url
         try to find a long link in the database
    """
    args = parse_args(sys.argv[1:])
    url = args.url
    generate = args.generate
    short_url = args.short_urlpylint
    with DB() as db:
        db.create_schema()
        if generate:
            if not short_url:
                short_url = shortuuid.uuid(url)
            if db.add_url(url, short_url):
                print(f'Short link to yours: {short_url}')
            else:
                print(f'Such a short link already exists: {short_url}')
        else:
            if long_url := db.select_long_url(url):
                print(long_url)
            else:
                print('There is no such link')


if __name__ == '__main__':
    main()
