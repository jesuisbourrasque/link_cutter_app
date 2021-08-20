import sys

import shortuuid

from db import DB


def main(url=None, short_url=None, generate=False):
    """
    if the user uses the --generate argument
        if the user uses the --short_urls argument with parameter short_url
            try to add data to the database
        else the user don't use --short_urls argument
            generate a short_url and try add to the database
    else the user input short_url
         try to find a long link in the database
    """
    url = url
    generate = generate
    short_url = short_url
    with DB() as db:
        db.create_schema()
        if generate:
            if not short_url:
                short_url = shortuuid.uuid(url)
            if db.add_url(url, short_url):
                return f'Short link to yours: {short_url}'
            else:
                return f'Such a short link already exists: {short_url}'
        else:
            if long_url := db.select_long_url(url):
                return long_url


if __name__ == '__main__':
    main()

