"""Dummy implementation of Tesserae API"""
import flask


APP = flask.Flask(__name__)


@APP.route('/query/corpora/languages', methods=['POST'])
def query_languages():
    return flask.jsonify(['Latin', 'Greek'])


@APP.route('/query/corpora/authors', methods=['POST'])
def query_authors():
    return flask.jsonify(['Vergil', 'Homer'])


@APP.route('/query/corpora/works', methods=['POST'])
def query_works():
    return flask.jsonify(['Aeneid', 'Odyssey'])


@APP.route('/query/corpora/works/books', methods=['POST'])
def query_books():
    return flask.jsonify(['1', '2', '3', '4', '5'])


@APP.route('/search', methods=['POST'])
def run_search():
    input_json = flask.request.get_json(force=True)
    return flask.jsonify(
        metadata={
            'service': 'Dummy',
            'version': '0.1',
            'feature': input_json['feature'],
        },
        results=[
            {
                'source CTS URN': '1',
                'target CTS URN': 'a',
                'score': 10.0,
            },
            {
                'source CTS URN': '2',
                'target CTS URN': 'b',
                'score': 5.3,
            },
        ]
    )
