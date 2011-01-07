#! /usr/bin/env python
from __future__ import with_statement

from flask import Flask, g, abort, url_for
import pymongo, pymongo.objectid
import datetime

from mojology.utils import templated

app = Flask (__name__)

config = {
    'mongodb': {
        'host': '10.9.8.1',
        'port': 27017,
        'db': 'syslog',
        'coll': 'messages'
    },
}

@app.template_filter ('datetime')
def datetimeformat (value, format='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.fromtimestamp (float (value)).strftime (format)

def mojology_page (page, hostname = None):
    if hostname:
        return url_for ('host', hostname = hostname, page = page)
    else:
        return url_for ('dashboard', page = page)

def mojology_dump (v, in_list = False, k = None):
    if type(v) == dict:
        r = "<table><thead><tr>"
        for key in v:
            r += "<th>%s</th>" % key
        r += "</tr></thead><tbody><tr>"
        for key in v:
            r += mojology_dump (v[key], True, key)
        r += "</tr></tbody></table>"
        return r
    else:
        if in_list:
            return "<td>%s</td>" % str (v)
        else:
            return str (v)

@app.before_request
def connect_mongo ():
    try:
        g.mongo = pymongo.Connection (config['mongodb']['host'], config['mongodb']['port'])
    except pymongo.errors.ConnectionFailure, e:
        abort (500)
    if not g.mongo[config['mongodb']['db']][config['mongodb']['coll']]:
        abort (500)
    g.coll = g.mongo[config['mongodb']['db']][config['mongodb']['coll']]

def get_logs (spec, page, extra = None):
    l = dict (logs = g.coll.find (spec = spec, sort = [('date', -1)],
                                  skip = (page - 1) * 15, limit = 15),
              maxpage = g.coll.find (spec = spec).count () / 15 + 1,
              page = page,
              mojology_page = mojology_page)
    if page > l['maxpage']:
        abort (404)
    if extra:
        l.update (extra)
    return l
    
@app.route ("/")
@app.route ("/page/<int(min=1):page>")
@templated ()
def dashboard (page = 1):
    return get_logs (None, page)

@app.route ("/about")
@app.route ("/about/")
@templated ()
def about ():
    return None

@app.route ("/host/<hostname>")
@app.route ("/host/<hostname>/page/<int(min=1):page>")
@templated ()
def host(hostname, page = 1):
    d = get_logs ({'host': hostname}, page, { 'hostname': hostname })
    if d['logs'].count () == 0:
        abort (404)
    return d

@app.route("/log/<logid>")
@templated ()
def log (logid):
    try:
        oid = pymongo.objectid.ObjectId (logid)
    except:
        abort (404)

    entry = g.coll.find_one (oid)

    if not entry:
        abort (404)

    return dict (log = entry, mojology_dump = mojology_dump)

if __name__ == "__main__":
    app.secret_key = '996ac3c8-19e2-11e0-806d-00248c0e4414'
    app.run (debug = True)
