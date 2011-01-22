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

## ---------------------------------------------
## - This file implements the statistics views -
## ---------------------------------------------
from mojology.utils import templated

from flask import Module, g, Markup, redirect, url_for
import pymongo.objectid, pymongo.json_util
import json
from pymongo.code import Code

statsm = Module (__name__)

@statsm.route ("/")
@templated ()
def index():
    return redirect (url_for ("stats.hosts"))

def _mr_dump (subtable):
    r = g.db[g.self_prefix + 'mr.' + subtable].find ()
    s = []
    for t in r:
        s.append (t)
    return Markup (json.dumps (s, default = pymongo.json_util.default))

@statsm.route ("/hosts")
@statsm.route ("/hosts/")
@templated ()
def hosts ():
    return dict (host_stats = _mr_dump ('hosts'))

@statsm.route ("/programs")
@statsm.route ("/programs/")
@templated ()
def programs ():
    return dict (prog_stats = _mr_dump ('programs'))

@statsm.route ("/time")
@statsm.route ("/time/")
@templated ()
def time ():
    return dict (time_stats = _mr_dump ('time'))
