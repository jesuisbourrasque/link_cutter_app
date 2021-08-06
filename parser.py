import argparse


def parse_args(args):
    """Parse console arguments"""
    parser = argparse.ArgumentParser(description='Url Cutter App')
    parser.add_argument('url', type=str, default=None, help='pass the url to cut it down')
    parser.add_argument('--generate', action='store_true', help='use this argument to generate short url')
    parser.add_argument('--short_url', type=str, default=None, help='enter a short version of your url')
    return parser.parse_args(args)
