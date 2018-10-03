"""Playground for testing flask features"""
import flask
from flask import request
import os


APP = flask.Flask(__name__)


@APP.route('/texts/<cts_urn>/')
def get_texts_other(cts_urn):
    print(cts_urn)
    return flask.jsonify(message='GET {}'.format(cts_urn))


@APP.route('/texts/')
def get_texts():
    print(request.args.get('works', ''))
    return flask.jsonify(message='GET texts')


if os.environ.get('ADMIN_INSTANCE'):
    @APP.route('/secret/')
    def get_secret():
        return flask.jsonify(message='GET secret')


    @APP.route('/texts/', methods=['DELETE'])
    def delete_texts():
        return flask.jsonify(message='DELETE texts', data=flask.request.form)
