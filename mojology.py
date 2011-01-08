#! /usr/bin/env python
##
## mojology - a syslog browser with style
## Copyright (C) 2011  Gergely Nagy <algernon@balabit.hu>
##
## Mojology is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## Mojology is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import Flask, g, abort, url_for, render_template, Markup
import pymongo, pymongo.objectid
import datetime, os

from mojology.utils import templated

app = Flask (__name__)
app.config.from_object ("mojology.default_config")
app.config.from_envvar ("MOJOLOGY_SETTINGS", True)
if os.path.exists ("local_settings.py"):
    app.config.from_pyfile ("local_settings.py")

@app.template_filter ('datetime')
def datetimeformat (value, format='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.fromtimestamp (float (value)).strftime (format)

def mojology_page (page, hostname = None):
    if hostname:
        return url_for ('host', hostname = hostname, page = page)
    else:
        return url_for ('dashboard', page = page)

def mojology_dump (v):
    if type(v) == dict:
        return Markup (render_template ("subtable.html", vars = v,
                                        mojology_dump = mojology_dump))
    else:
        return str (v)

@app.before_request
def connect_mongo ():
    try:
        g.mongo = pymongo.Connection (app.config['MONGO_HOST'], app.config['MONGO_PORT'])
    except pymongo.errors.ConnectionFailure, e:
        abort (500)
    g.coll = g.mongo[app.config['MONGO_DB']][app.config['MONGO_COLLECTION']]
    if not g.coll:
        abort (500)

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

    return dict (logs = [ entry ], mojology_dump = mojology_dump,
                 dyn_vars = entry[app.config['MONGO_DYNVARS']])

if __name__ == "__main__":
    app.run ()
