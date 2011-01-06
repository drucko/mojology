#! /usr/bin/env python
from __future__ import with_statement

from flask import Flask, render_template, g
import pymongo, pymongo.objectid

app = Flask (__name__)

@app.before_request
def connect_mongo ():
    try:
        g.mongo = pymongo.Connection ("10.9.8.1", 27017)
    except pymongo.errors.ConnectionFailure, e:
        return "Unable to connect to MongoDB instance."

@app.route ("/")
def dashboard ():
    logs = g.mongo['syslog'].messages.find (sort = [('date', -1)], limit = 15)
    return render_template ("index.html", logs = logs)

@app.route("/log/<logid>")
def log (logid):
    entry = g.mongo['syslog'].messages.find_one (pymongo.objectid.ObjectId(logid))
    print entry
    return render_template ('log.html', log = entry)

if __name__ == "__main__":
    app.secret_key = '996ac3c8-19e2-11e0-806d-00248c0e4414'
    app.run (debug = True)
