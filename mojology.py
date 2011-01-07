#! /usr/bin/env python
from __future__ import with_statement

from flask import Flask, render_template, g, abort
import pymongo, pymongo.objectid

app = Flask (__name__)

config = {
    'mongodb': {
        'host': '10.9.8.1',
        'port': 27017,
        'db': 'syslog',
        'coll': 'messages'
    },
}

@app.before_request
def connect_mongo ():
    try:
        g.mongo = pymongo.Connection (config['mongodb']['host'], config['mongodb']['port'])
    except pymongo.errors.ConnectionFailure, e:
        abort (500)
    if not g.mongo[config['mongodb']['db']][config['mongodb']['coll']]:
        abort (500)
    g.coll = g.mongo[config['mongodb']['db']][config['mongodb']['coll']]

@app.route ("/")
def dashboard ():
    logs = g.coll.find (sort = [('date', -1)], limit = 15)
    return render_template ("index.html", logs = logs)

@app.route("/host/<hostname>")
def host(hostname):
    logs = g.coll.find (spec = {'host': hostname},
                        sort = [('date', -1)], limit = 15)
    if logs.count () == 0:
        abort (404)
    return render_template ("host.html", logs = logs,
                            hostname = hostname)

@app.route("/log/<logid>")
def log (logid):
    try:
        oid = pymongo.objectid.ObjectId (logid)
    except:
        abort (404)

    entry = g.coll.find_one (oid)

    if not entry:
        abort (404)

    return render_template ('log.html', log = entry)

if __name__ == "__main__":
    app.secret_key = '996ac3c8-19e2-11e0-806d-00248c0e4414'
    app.run (debug = True)
