"""Script to print output from Tesserae API server"""
import argparse
import requests


def _parse_args():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Template file')
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='host name')
    parser.add_argument(
        '--port',
        default='5000',
        help='server port')
    return parser.parse_args()


def _query_languages(base_url):
    """Queries server for languages"""
    req = requests.post(
        base_url + '/query/corpora/languages',
        data={}
    )
    print(req.json())


def _run():
    """Runs queries against Tesserae API server"""
    args = _parse_args()
    base_url = 'http://' + args.host + ':' + args.port
    _query_languages(base_url)


if __name__ == '__main__':
    _run()
