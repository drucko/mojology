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

## ----------------------------------------------
## - This file implements the log browser views -
## ----------------------------------------------
from mojology.utils import templated

from flask import Module, g, url_for, render_template, Markup, abort
import pymongo.objectid

browser = Module (__name__)

def url_for_page (page, hostname = None):
    if hostname:
        return url_for ('host', hostname = hostname, page = page)
    else:
        return url_for ('dashboard', page = page)

def log_entry_dump (v):
    if type(v) == dict:
        return Markup (render_template ("browser/subtable.html", vars = v,
                                        mojology_dump = log_entry_dump))
    else:
        return str (v)

def get_logs (spec, page, extra = None):
    l = dict (logs = g.coll.find (spec = spec, sort = [('ts', -1)],
                                  skip = (page - 1) * g.pagesize,
                                  limit = g.pagesize),
              maxpage = g.coll.find (spec = spec).count () / g.pagesize + 1,
              page = page,
              mojology_page = url_for_page)
    if page > l['maxpage']:
        abort (404)
    if extra:
        l.update (extra)
    return l
    
@browser.route ("/")
@browser.route ("/page/<int(min=1):page>")
@templated ()
def dashboard (page = 1):
    return get_logs (None, page)

@browser.route ("/host/<hostname>/")
@browser.route ("/host/<hostname>/page/<int(min=1):page>")
@templated ()
def host(hostname, page = 1):
    d = get_logs ({'host': hostname}, page, { 'hostname': hostname })
    if d['logs'].count () == 0:
        abort (404)
    return d

@browser.route("/log/<logid>")
@templated ()
def log (logid):
    try:
        oid = pymongo.objectid.ObjectId (logid)
    except:
        abort (404)

    entry = g.coll.find_one (oid)

    if not entry:
        abort (404)

    return dict (log = entry, mojology_dump = log_entry_dump,
                 dyn_vars = entry[g.dyn_vars])

@browser.route ("/log/<logid>/dyn")
def log_dyn (logid):
    return log (logid)
