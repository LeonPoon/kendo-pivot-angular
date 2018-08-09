#!/usr/bin/env python3

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import json
import os
import regex

app = Flask(__name__)
CORS(app)


demo = os.path.join(os.path.dirname(__file__), '..', 'demo')


def deserialise_jquery_to(obj, pk, k_gen, v):
    k = next(k_gen, None)
    if k:
        try:
            k = int(k)
            is_int = True
        except ValueError:
            is_int = False
        if is_int:
            if obj is None:
                obj = []
            if len(obj) <= k:
                obj.extend((None,) * (k - len(obj) + 1))
            o = obj[k]
        else:
            if obj is None:
                obj = {}
            o = obj.get(k)
        obj[k] = deserialise_jquery_to(o, k, k_gen, v)
    elif k == '':
        if obj is None:
            obj = [v]
        else:
            obj.append(v)
    elif k is None:
        obj = v
    return obj


def deserialise_jquery(args, re=regex.compile('^([A-Za-z_][A-Za-z0-9_]*)(?:\\[((?:0|[1-9][0-9]*)|(?:[A-Za-z_][A-Za-z0-9_]*)*)\\])*$')):
    obj = {}
    for k, v in args.items():
        match = re.match(k)
        if match:
            (k,), ks = [match.captures(i) for i in range(1, len(match.groups()) + 1)]
            deserialise_jquery_to(obj, None, (k for k in ((k,), ks) for k in k), (v == 'true') if v in ('true', 'false') else v)
    return obj


@app.route('/')
def index():
    args = deserialise_jquery(request.args)
    data = None
    for f in os.listdir(demo):
        with open(os.path.join(demo, f), 'r') as f:
            f = json.load(f)
        if f['read'] == args:
            data = f['data']
    if data is None:
        abort(404)
    return jsonify(data)
