#!/usr/bin/env python3

from flask import Flask, request, jsonify, abort, Request
from flask_cors import CORS
import json
import os
from werkzeug.datastructures import ImmutableOrderedMultiDict
from deserialise_jquery_param import deserialise_jquery_param


class MyRequest(Request):
    """Request subclass to override request parameter storage"""
    parameter_storage_class = ImmutableOrderedMultiDict


class MyFlask(Flask):
    """Flask subclass using the custom request class"""
    request_class = MyRequest


app = MyFlask(__name__)
CORS(app)


demo = os.path.join(os.path.dirname(__file__), '..', 'demo')


@app.route('/')
def index():
    args = deserialise_jquery_param(request.args.items(multi=True))
    data = None
    for f in os.listdir(demo):
        with open(os.path.join(demo, f), 'r') as f:
            f = json.load(f)
        if f['read'] == args:
            data = f['data']
    if data is None:
        abort(404)
    return jsonify(data)
