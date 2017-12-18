"""Script to print output from Tesserae API server"""
import argparse
from functools import wraps
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


def _query(base_url, endpoint, data):
    """Returns json obtained from endpoint with given data"""
    req = requests.post(base_url + endpoint, json=data)
    return req.json()


def _query_languages(base_url):
    """Returns languages query response from server"""
    return _query(
        base_url,
        '/query/corpora/languages',
        {}
    )


def _query_authors(base_url):
    """Returns authors query response from server"""
    return _query(
        base_url,
        '/query/corpora/authors',
        {}
    )


def _query_works(base_url):
    """Returns works query response from server"""
    return _query(
        base_url,
        '/query/corpora/works',
        {}
    )


def _query_books(base_url, work_metadata):
    """Returns books query response from server"""
    return _query(
        base_url,
        '/query/corpora/works/books',
        work_metadata
    )


def _search(base_url, search_options):
    """Returns search results response from server"""
    return _query(
        base_url,
        '/search',
        search_options
    )


def _run():
    """Runs queries against Tesserae API server"""
    args = _parse_args()
    base_url = 'http://' + args.host + ':' + args.port
    print(_query_languages(base_url))
    print(_query_authors(base_url))
    print(_query_works(base_url))
    print(_query_books(base_url,
        {
            'language': 'Latin',
            'author': 'Vergil',
            'work': 'Aeneid'
        }
    ))
    print(_search(base_url,
        {
            'source CTS URN': '1',
            'target CTS URN': '2',
            'feature': 'stem'
        }
    ))


if __name__ == '__main__':
    _run()
