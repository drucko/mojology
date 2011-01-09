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

from flask import Module, g, Markup
import pymongo.objectid, pymongo.json_util
import json

statsm = Module (__name__)

@statsm.route ("/")
@templated ()
def dashboard ():
    host_stats = g.coll.group (["host"], {}, {"count": 0 }, "function (obj, prev) { prev.count++; }");
    return dict (host_stats = Markup (json.dumps (host_stats, default = pymongo.json_util.default)))

@statsm.route ("/programs")
@statsm.route ("/programs/")
@templated ()
def programs ():
    prog_stats = g.coll.group (["program.name"], {}, {"count": 0},
                               "function (obj, prev) { prev.count++; }");
    return dict (prog_stats = Markup (json.dumps (prog_stats, default = pymongo.json_util.default)))
