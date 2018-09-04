"""Dummy implementation of Tesserae API"""
import flask

import tesserae.db
import tesserae.text_access.storage
import tesserae.tokenizers.tokenize
import tesserae.unitizers


APP = flask.Flask(__name__)
HOST = '127.0.0.1'
PORT = 27017
USER = None
PASSWORD = None


def db_error(message):
    response = flask.jsonify(message=message)
    response.status_code = 500
    return response


def user_error(message):
    response = flask.jsonify(message=message)
    response.status_code = 400
    return response


@APP.route('/texts/', defaults={'language': None, 'author': None, 'text': None})
@APP.route('/texts/<language>/', defaults={'author': None, 'text': None})
@APP.route('/texts/<language>/<author>/', defaults={'text': None})
@APP.route('/texts/<language>/<author>/<text>')
def get_texts(language, author, text):
    # TODO update tesserae-v5 repo when fix to filtering bug is committed
    client = tesserae.db.get_connection(HOST, PORT, USER, PASSWORD)
    db_response = tesserae.text_access.storage.retrieve_text_list(client, language=language, author=author, title=text)
    result = {'texts': {}}
    for doc in db_response:
        cur_lang = doc.language
        if cur_lang not in result['texts']:
            result['texts'][cur_lang] = {}
        cur_author = doc.author
        if cur_author not in result['texts'][cur_lang]:
            result['texts'][cur_lang][cur_author] = []
        result['texts'][cur_lang][cur_author].append({
            'id': doc.cts_urn,
            'title': doc.title,
            'metadata': {
                'year': doc.year,
                'unit_types': doc.unit_types,
            },
        })
    client.close()
    return flask.jsonify(result)


@APP.route('/texts/<language>/<author>/<text>', methods=['POST'])
def post_text(language, author, text):
    # TODO figure out authentication
    data = flask.request.form
    try:
        client = tesserae.db.get_connection(HOST, PORT, USER, PASSWORD)
        db_response = tesserae.text_access.storage.retrieve_text_list.insert_text(
            client,
            data['cts_urn'],
            data['language'],
            data['author'],
            data['title'],
            int(data['year']),
            data['unit_types'],
            data['path'],
        )
    except tesserae.text_access.storage.TextExistsError as e:
        return user_error(e.args)
    finally:
        client.close()
    if not db_response.acknowledged:
        return db_error('Database error')

    # TODO work queue? text processing?
    return flask.jsonify(flask.request.form)


# TODO figure out session handling?
@APP.route('/texts/<language>/<author>/<text>', methods=['PUT'])
def update_text(language, author, text):
    # TODO it seems like the type checking should be done in update_text
    accepted_metadata = {
        'language',
        'author',
        'title',
        'year',
        'path',
        'hash',
    }
    data = flask.request.form
    # TODO update 'id' to 'cts_urn' for consistency with database?
    if 'id' not in data:
        return user_error('No "id": please provide CTS URN')
    cts_urn = data['id']
    diff = {k for k in data} - accepted_metadata
    diff.remove('id')
    if diff:
        return user_error('Unknown metadata types: {}'.format(', '.join(diff)))
    try:
        client = tesserae.db.get_connection(HOST, PORT, USER, PASSWORD)
        db_response = tesserae.text_access.storage.update_text(
            client,
            cts_urn,
            **{k: v for k, v in data.items() if k != 'id'},
        )
    except tesserae.text_access.storage.DuplicateTextError as e:
        return db_error(e.args)
    except Exception as e:
        return user_error(e.args)
    finally:
        client.close()
    if not db_response.acknowledged:
        return db_error('Database error')
    # TODO negotiate database updating
    # work queue?
    return flask.jsonify(db_response.raw_result)


# TODO figure out session handling?
@APP.route('/texts/<language>/<author>/<text>', methods=['DELETE'])
def delete_text(language, author, text):
    # TODO negotiate database updating
    # TODO implement deleting in tesserae.text_access.storage
    client = tesserae.db.get_connection(HOST, PORT, USER, PASSWORD)
    client.close()
    return flask.jsonify(flask.request.form)


@APP.route('/tokens/<text>/<feature>', defaults={'unit': None})
@APP.route('/tokens/<text>/<feature>/<unit>')
def get_tokens(feature, unit):
    # TODO should 'text' be 'cts_urn'?
    try:
        client = tesserae.db.get_connection(HOST, PORT, USER, PASSWORD)
        found = tesserae.text_access.storage.retrieve_text_list(client, title=text)[0]
        result = {
            'title': found['title'],
            'author': found['author'],
            'language': found['language'],
            'id': found['cts_urn'],
            'metadata': {
                'year': found['year'],
                'unit_types': found['unit_types'],
            },
        }
        tessfile = tesserae.text_access.storage.load_text(client, found['cts_urn'])
        # TODO how to know whether text is poetry or prose
        # TODO finish implementing once library has been fleshed out
        if unit is None:
            if tessfile.metadata.get('genre', None) == 'poetry':
                result['phrases'] = [
                    unit['tokens'] for unit in tesserae.unitizers.poetry.split_phrase_units()
                ]
        tokenized = [tesserae.tokenizers.tokenize.get_token_info(token, tessfile.metadata.language) for token in tessfile.read_tokens()]
    finally:
    client.close()
    return flask.jsonify(result)
