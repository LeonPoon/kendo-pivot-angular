#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)


expand2006 = {
  "rows[0][name][]": [
    "[Geography].[City].[All Geographies]"
  ],
  "columns[0][name][]": [
    "[Date].[Calendar].[Calendar Year].&[2006]"
  ],
  "columns[1][expand]": [
    "false"
  ],
  "columns[0][expand]": [
    "true"
  ],
  "measuresAxis": [
    "columns"
  ],
  "rows[0][expand]": [
    "false"
  ],
  "columns[1][name][]": [
    "[Product].[Category].[All Products]"
  ]
}


expand_geog = {
  "columns[1][expand]": [
    "true"
  ],
  "columns[2][expand]": [
    "false"
  ],
  "columns[2][name][]": [
    "[Product].[Category].[All Products]"
  ],
  "columns[1][name][]": [
    "[Date].[Calendar].[Calendar Year].&[2006]"
  ],
  "rows[0][expand]": [
    "true"
  ],
  "measuresAxis": [
    "columns"
  ],
  "columns[0][expand]": [
    "true"
  ],
  "columns[0][name][]": [
    "[Date].[Calendar].[All Periods]"
  ],
  "rows[0][name][]": [
    "[Geography].[City].[All Geographies]"
  ]
}


demo = os.path.join(os.path.dirname(__file__), '..', 'demo')


@app.route('/')
def index():
    print(dict(request.args))
    path = None
    if request.args == {'measuresAxis': ['columns']}:
        path = os.path.join(demo, 'demo1.json')
    elif request.args == expand2006:
        path = os.path.join(demo, 'demo2-expand-2006.json')
    elif request.args == expand_geog:
        path = os.path.join(demo, 'demo3-expand-all-geog.json')
    if path:
        with open(path, 'r') as data:
            data = json.load(data)
    else:
        data = {}
    return jsonify(data)
