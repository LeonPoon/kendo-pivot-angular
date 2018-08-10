#!/usr/bin/env python3

from flask import Flask, request, jsonify, abort, Request
from flask_cors import CORS
import json
import os
import regex
import unittest
from werkzeug.datastructures import ImmutableOrderedMultiDict


class MyRequest(Request):
    """Request subclass to override request parameter storage"""
    parameter_storage_class = ImmutableOrderedMultiDict


class MyFlask(Flask):
    """Flask subclass using the custom request class"""
    request_class = MyRequest


app = MyFlask(__name__)
CORS(app)


demo = os.path.join(os.path.dirname(__file__), '..', 'demo')


def deserialise_jquery_to(obj, k_gen, v):
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
            o = k - len(obj) + 1
            if o > 0:
                obj.extend((None,) * o)
            o = obj[k]
        else:
            if obj is None:
                obj = {}
            o = obj.get(k)
        obj[k] = deserialise_jquery_to(o, k_gen, v)
    elif k is '':
        if obj is None:
            obj = [v]
        else:
            obj.append(v)
    elif k is None:
        obj = v
    return obj


def deserialise_jquery(args, re=regex.compile('^([A-Za-z_][A-Za-z0-9_]*)(?:\\[((?:0|[1-9][0-9]*)|(?:[A-Za-z_][A-Za-z0-9_]*)*)\\])*$')):
    obj = {}
    for k, v in args.items(multi=True):
        match = re.match(k)
        if match:
            ks = (match.captures(i) for i in range(1, len(match.groups()) + 1))
            obj = deserialise_jquery_to(obj, (k for ks in ks for k in ks), (v == 'true') if v in ('true', 'false') else v)
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



class DeserialiseJQueryTest(unittest.TestCase):

    from werkzeug.wrappers import url_decode, BaseRequest
    import pprint

    test_num = 0

    true = True
    false = False
    undefined = object()
    null = object()

    class jQuery(object):

        @classmethod
        def param(cls, params, old=False):
            return (params, cls.params(params), old)

        @classmethod
        def params(cls, params):
            if callable(getattr(params, 'append', None)):
                return list(map(cls.params, params))
            elif callable(getattr(params, 'keys', None)):
                return dict(cls.de_dupe(k, cls.params(params[k])) for k in params.keys())
            elif params is DeserialiseJQueryTest.true or params is DeserialiseJQueryTest.false:
                return params
            elif params in (DeserialiseJQueryTest.undefined, DeserialiseJQueryTest.null):
                return ''
            elif callable(params):
                return cls.params(params())
            else:
                return str(params)

        @classmethod
        def de_dupe(cls, k, v):
            while k.endswith(']'):
                pos = k.rfind('[')
                k, k2 = k[:pos], k[pos + 1:-1]
                if k2:
                    v = {k2: v}
            return (k, v)

        @classmethod
        def decodeURIComponent(cls, params):
            return params

    @classmethod
    def make_func(cls, params, query_string, msg):
        original, params, old = params
        @unittest.skipIf(old, reason='old')
        def test(self):
            return self.do_it(original, params, old, query_string, msg)
        cls.test_num = test_num = cls.test_num + 1
        setattr(cls, 'test_%d old=%s: %s' % (test_num, old, msg), test)

    def do_it(self, original, params, old, query_string, msg):
        cls = self.__class__
        args = cls.url_decode(query_string, cls.BaseRequest.charset, errors=cls.BaseRequest.encoding_errors, cls=MyRequest.parameter_storage_class)
        d = deserialise_jquery(args)
        self.assertEqual(params if query_string else {}, d,
            '%s:\n\noriginal:\n%s\n\nexpect:\n%s\n\ngot:\n%s' % (msg, cls.pprint.pformat(original), cls.pprint.pformat(params), cls.pprint.pformat(d)))

    @classmethod
    def init(cls):

        true = cls.true
        false = cls.false
        undefined = cls.undefined
        null = cls.null

        assert_equal = cls.make_func
        jQuery = cls.jQuery
        decodeURIComponent = jQuery.decodeURIComponent

        a,b,c,d,e,f,g,h,i,j,k,l,m,_,_,_,_,_,_,_,_,_,_,x,y,z = 'abcdefghijklmnopqrstuvwxyz'

        ### Below from: https://github.com/jquery/jquery/blob/0645099e027cd0e31a828572169a8c25474e2b5c/test/unit/serialize.js

        params = { "foo":"bar", "baz":42, "quux":"All your base are belong to us" }
        assert_equal( jQuery.param( params ), "foo=bar&baz=42&quux=All%20your%20base%20are%20belong%20to%20us", "simple" )

        params = { "string":"foo", "null":null, "undefined":undefined }
        assert_equal( jQuery.param( params ), "string=foo&null=&undefined=", "handle nulls and undefineds properly" )

        params = { "someName": [ 1, 2, 3 ], "regularThing": "blah" }
        assert_equal( jQuery.param( params ), "someName%5B%5D=1&someName%5B%5D=2&someName%5B%5D=3&regularThing=blah", "with array" )

        params = { "foo": [ "a", "b", "c" ] }
        assert_equal( jQuery.param( params ), "foo%5B%5D=a&foo%5B%5D=b&foo%5B%5D=c", "with array of strings" )

        params = { "foo": [ "baz", 42, "All your base are belong to us" ] }
        assert_equal( jQuery.param( params ), "foo%5B%5D=baz&foo%5B%5D=42&foo%5B%5D=All%20your%20base%20are%20belong%20to%20us", "more array" )

        params = { "foo": { "bar": "baz", "beep": 42, "quux": "All your base are belong to us" } }
        assert_equal( jQuery.param( params ), "foo%5Bbar%5D=baz&foo%5Bbeep%5D=42&foo%5Bquux%5D=All%20your%20base%20are%20belong%20to%20us", "even more arrays" )

        params = { a:[ 1, 2 ], b:{ c:3, d:[ 4, 5 ], e:{ x:[ 6 ], y:7, z:[ 8, 9 ] }, f:true, g:false, h:undefined }, i:[ 10, 11 ], j:true, k:false, l:[ undefined, 0 ], m:"cowboy hat?" }
        assert_equal( decodeURIComponent( jQuery.param( params ) ), "a[]=1&a[]=2&b[c]=3&b[d][]=4&b[d][]=5&b[e][x][]=6&b[e][y]=7&b[e][z][]=8&b[e][z][]=9&b[f]=true&b[g]=false&b[h]=&i[]=10&i[]=11&j=true&k=false&l[]=&l[]=0&m=cowboy hat?", "huge structure" )

        params = { "a": [ 0, [ 1, 2 ], [ 3, [ 4, 5 ], [ 6 ] ], { "b": [ 7, [ 8, 9 ], [ { "c": 10, "d": 11 } ], [ [ 12 ] ], [ [ [ 13 ] ] ], { "e": { "f": { "g": [ 14, [ 15 ] ] } } }, 16 ] }, 17 ] }
        assert_equal( decodeURIComponent( jQuery.param( params ) ), "a[]=0&a[1][]=1&a[1][]=2&a[2][]=3&a[2][1][]=4&a[2][1][]=5&a[2][2][]=6&a[3][b][]=7&a[3][b][1][]=8&a[3][b][1][]=9&a[3][b][2][0][c]=10&a[3][b][2][0][d]=11&a[3][b][3][0][]=12&a[3][b][4][0][0][]=13&a[3][b][5][e][f][g][]=14&a[3][b][5][e][f][g][1][]=15&a[3][b][]=16&a[]=17", "nested arrays" )

        params = { "a":[ 1, 2 ], "b":{ "c":3, "d":[ 4, 5 ], "e":{ "x":[ 6 ], "y":7, "z":[ 8, 9 ] }, "f":true, "g":false, "h":undefined }, "i":[ 10, 11 ], "j":true, "k":false, "l":[ undefined, 0 ], "m":"cowboy hat?" }
        assert_equal( jQuery.param( params, true ), "a=1&a=2&b=%5Bobject%20Object%5D&i=10&i=11&j=true&k=false&l=&l=0&m=cowboy%20hat%3F", "huge structure, forced traditional" )

        assert_equal( decodeURIComponent( jQuery.param( { "a": [ 1, 2, 3 ], "b[]": [ 4, 5, 6 ], "c[d]": [ 7, 8, 9 ], "e": { "f": [ 10 ], "g": [ 11, 12 ], "h": 13 } } ) ), "a[]=1&a[]=2&a[]=3&b[]=4&b[]=5&b[]=6&c[d][]=7&c[d][]=8&c[d][]=9&e[f][]=10&e[g][]=11&e[g][]=12&e[h]=13", "Make sure params are not double-encoded." )

        #7945
        assert_equal( jQuery.param( { "jquery": "1.4.2" } ), "jquery=1.4.2", "Check that object with a jQuery property get serialized correctly" )

        params = { "foo":"bar", "baz":42, "quux":"All your base are belong to us" }
        assert_equal( jQuery.param( params, true ), "foo=bar&baz=42&quux=All%20your%20base%20are%20belong%20to%20us", "simple" )

        params = { "someName": [ 1, 2, 3 ], "regularThing": "blah" }
        assert_equal( jQuery.param( params, true ), "someName=1&someName=2&someName=3&regularThing=blah", "with array" )

        params = { "foo": [ "a", "b", "c" ] }
        assert_equal( jQuery.param( params, true ), "foo=a&foo=b&foo=c", "with array of strings" )

        params = { "foo[]":[ "baz", 42, "All your base are belong to us" ] }
        assert_equal( jQuery.param( params, true ), "foo%5B%5D=baz&foo%5B%5D=42&foo%5B%5D=All%20your%20base%20are%20belong%20to%20us", "more array" )

        params = { "foo[bar]":"baz", "foo[beep]":42, "foo[quux]":"All your base are belong to us" }
        assert_equal( jQuery.param( params, true ), "foo%5Bbar%5D=baz&foo%5Bbeep%5D=42&foo%5Bquux%5D=All%20your%20base%20are%20belong%20to%20us", "even more arrays" )

        params = { a:[ 1, 2 ], b:{ c:3, d:[ 4, 5 ], e:{ x:[ 6 ], y:7, z:[ 8, 9 ] }, f:true, g:false, h:undefined }, i:[ 10, 11 ], j:true, k:false, l:[ undefined, 0 ], m:"cowboy hat?" }
        assert_equal( jQuery.param( params, true ), "a=1&a=2&b=%5Bobject%20Object%5D&i=10&i=11&j=true&k=false&l=&l=0&m=cowboy%20hat%3F", "huge structure" )

        params = { "a": [ 0, [ 1, 2 ], [ 3, [ 4, 5 ], [ 6 ] ], { "b": [ 7, [ 8, 9 ], [ { "c": 10, d: 11 } ], [ [ 12 ] ], [ [ [ 13 ] ] ], { "e": { "f": { "g": [ 14, [ 15 ] ] } } }, 16 ] }, 17 ] }
        assert_equal( jQuery.param( params, true ), "a=0&a=1%2C2&a=3%2C4%2C5%2C6&a=%5Bobject%20Object%5D&a=17", "nested arrays (not possible when traditional == true)" )

        params = { a:[ 1, 2 ], b:{ c:3, d:[ 4, 5 ], e:{ x:[ 6 ], y:7, z:[ 8, 9 ] }, f:true, g:false, h:undefined }, i:[ 10, 11 ], j:true, k:false, l:[ undefined, 0 ], m:"cowboy hat?" }
        assert_equal( decodeURIComponent( jQuery.param( params ) ), "a[]=1&a[]=2&b[c]=3&b[d][]=4&b[d][]=5&b[e][x][]=6&b[e][y]=7&b[e][z][]=8&b[e][z][]=9&b[f]=true&b[g]=false&b[h]=&i[]=10&i[]=11&j=true&k=false&l[]=&l[]=0&m=cowboy hat?", "huge structure, forced not traditional" )

        params = { "param1": null }
        assert_equal( jQuery.param( params ), "param1=", "Make sure that null params aren't traversed." )

        params = { "param1": lambda: null, "param2": lambda: null }
        assert_equal( jQuery.param( params, false ), "param1=&param2=", "object with function property that returns null value" )

        params = { "test": { "length": 3, "foo": "bar" } }
        assert_equal( jQuery.param( params ), "test%5Blength%5D=3&test%5Bfoo%5D=bar", "Sub-object with a length property" )

        params = { "test": [ 1, 2, null ] }
        assert_equal( jQuery.param( params ), "test%5B%5D=1&test%5B%5D=2&test%5B%5D=", "object with array property with null value" )

        params = undefined
        assert_equal( jQuery.param( params ), "", "jQuery.param( undefined ) === empty string" )


DeserialiseJQueryTest.init()
if __name__ == '__main__':
    import nose
    nose.main(argv=[__name__, __file__])
