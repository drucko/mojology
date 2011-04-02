#! /usr/bin/env python
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

from mojology import Mojology
import pymongo
import os

cfg_file = os.path.realpath (os.path.join (os.path.dirname (__file__), "local_settings.py"))
if not os.path.exists (cfg_file):
    cfg_file = None

m = Mojology (config_file = cfg_file)

conn = pymongo.Connection (m.config['MONGO_HOST'], m.config['MONGO_PORT'])
db = conn[m.config['MONGO_DB']]
coll = db[m.config['MONGO_COLLECTION']]
cache = m.config['MOJOLOGY_COLLECTION_PREFIX']
layout = m.config['MOJOLOGY_LAYOUT']

def mr (map_js, out):
    coll.map_reduce (map_js,
                     "function (k, vals) { var sum = { count: 0 }; for (var i in vals) sum.count += vals[i].count; return sum; }",
                     out = cache + 'mr.' + out,
                     finalize = "function (who, res) { res.stamp = new Date(); return res; }")

mr ("function () { emit(this.%s, { count: 1 }); }" % layout.fields['program'], "programs")
mr ("function () { emit(this.%s, { count: 1 }); }" % layout.fields['host'], "hosts")
mr ("function () { var d = new Date (this.%s*1000); d.setMinutes(0); d.setSeconds(0); emit(d.valueOf(), { count: 1 }); }" % layout.fields['date'],
    "time")
