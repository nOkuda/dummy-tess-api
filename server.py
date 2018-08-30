"""Dummy implementation of Tesserae API"""
import flask

import tesserae.db
import tesserae.text_access.storage


APP = flask.Flask(__name__)
HOST = '127.0.0.1'
PORT = 27017
USER = None
PASSWORD = None
CLIENT = tesserae.db.get_connection(HOST, PORT, USER, PASSWORD)


@APP.route('/texts/', defaults={'language': None, 'author': None, 'text': None})
@APP.route('/texts/<language>/', defaults={'author': None, 'text': None})
@APP.route('/texts/<language>/<author>/', defaults={'text': None})
@APP.route('/texts/<language>/<author>/<text>')
def get_texts(language, author, text):
    # TODO fix bug (filtering on author doesn't work, though filtering on language does)
    print(language, author, text)
    db_response = tesserae.text_access.storage.retrieve_text_list(CLIENT, language=language, author=author, title=text)
    print(db_response)
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
    return flask.jsonify(result)


@APP.route('/texts/<language>/<author>/<text>', methods=['POST'])
def post_text(language, author, text):
    # TODO figure out authentication
    data = flask.request.form
    try:
        db_response = tesserae.text_access.storage.retrieve_text_list.insert_text(
            data['cts_urn'],
            data['language'],
            data['author'],
            data['title'],
            int(data['year']),
            data['unit_types'],
            data['path'],
        )
    except tesserae.text_access.storage.TextExistsError as e:
        response = flask.jsonify(message=e.args)
        response.status_code = 400
        return response
    if not db_response.acknowledged:
        response = flask.jsonify(message='Database error')
        response.status_code = 500
        return response

    # TODO work queue? text processing?
    return flask.jsonify(flask.request.form)


# TODO figure out session handling?
@APP.route('/texts/<language>/<author>/<text>', methods=['PUT'])
def update_text(language, author, text):
    data = flask.request.form
    if 'cts_urn' not in data:
        response = flask.jsonify(message='No cts_urn')
        response.status_code = 400
        return response
    cts_urn = data['cts_urn']
    del data['cts_urn']
    try:
        db_response = tesserae.text_access.storage.update_text(
            CLIENT,
            cts_urn,
            **data,
        )
    except tesserae.text_access.storage.DuplicateTextError as e:
        response = flask.jsonify(message=e.args)
        response.status_code = 500
        return response
    except e:
        response = flask.jsonify(message=e.args)
        response.status_code = 400
        return response
    if not db_response.acknowledged:
        response = flask.jsonify(message='Database error')
        response.status_code = 500
        return response
    # TODO negotiate database updating
    # work queue?
    return flask.jsonify(db_response.raw_result)


# TODO figure out session handling?
@APP.route('/texts/<language>/<author>/<text>', methods=['DELETE'])
def delete_text(language, author, text):
    # TODO negotiate database updating
    # TODO implement deleting in tesserae.text_access.storage
    return flask.jsonify(flask.request.form)
