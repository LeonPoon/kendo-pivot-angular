#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)


expand2006 = {
  "columns[0][name][]": [
    "[Date].[Calendar].[Calendar Year].&[2006]"
  ],
  "columns[0][expand]": [
    "true"
  ],
  "columns[1][name][]": [
    "[Product].[Category].[All Products]"
  ],
  "columns[1][expand]": [
    "false"
  ],
  "rows[0][name][]": [
    "[Geography].[City].[All Geographies]"
  ],
  "rows[0][expand]": [
    "false"
  ],
  "measuresAxis": [
    "columns"
  ]
}


expand_geog = {
  "columns[0][name][]": [
    "[Date].[Calendar].[All Periods]"
  ],
  "columns[0][expand]": [
    "true"
  ],
  "columns[1][name][]": [
    "[Date].[Calendar].[Calendar Year].&[2006]"
  ],
  "columns[1][expand]": [
    "true"
  ],
  "columns[2][name][]": [
    "[Product].[Category].[All Products]"
  ],
  "columns[2][expand]": [
    "false"
  ],
  "rows[0][name][]": [
    "[Geography].[City].[All Geographies]"
  ],
  "rows[0][expand]": [
    "true"
  ],
  "measuresAxis": [
    "columns"
  ]
}


expand2008 = {
  "columns[0][name][]": [
    "[Date].[Calendar].[Calendar Year].&[2008]"
  ],
  "columns[0][expand]": [
    "true"
  ],
  "columns[1][name][]": [
    "[Product].[Category].[All Products]"
  ],
  "columns[1][expand]": [
    "false"
  ],
  "measuresAxis": [
    "columns"
  ],
  "rows[0][name][]": [
    "[Geography].[City].[All Geographies]"
  ],
  "rows[0][expand]": [
    "true"
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
    elif request.args == expand2008:
        path = os.path.join(demo, 'demo3-expand-2008.json')
    if path:
        with open(path, 'r') as data:
            data = json.load(data)
    else:
        data = {}
    return jsonify(data)
