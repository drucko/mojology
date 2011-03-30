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
from mojology.config import Columnizer
import unittest
import pymongo, pymongo.json_util
import json
import os

class TestConfig (object):
    DEBUG = True
    TESTING = True
    MONGO_HOST = "127.0.0.1"
    MONGO_PORT = 27017
    MONGO_DB = "mojology_test"
    MONGO_COLLECTION = "messages"

    MOJOLOGY_PAGESIZE = 10
    MOJOLOGY_COLLECTION_PREFIX = "mojology."

    MOJOLOGY_COLUMNIZER = Columnizer ()

class TestCase (unittest.TestCase):
    def setUp (self):
        self.mojology = Mojology (config_object = "mojology.tests.TestConfig")
        self.app = self.mojology.test_client ()

        self.db = pymongo.Connection (TestConfig.MONGO_HOST, TestConfig.MONGO_PORT)
        self.coll = self.db[TestConfig.MONGO_DB][TestConfig.MONGO_COLLECTION]
        self.pagesize = TestConfig.MOJOLOGY_PAGESIZE
        self.cache = TestConfig.MOJOLOGY_COLLECTION_PREFIX
        self.columnizer = TestConfig.MOJOLOGY_COLUMNIZER

        self.coll.drop ()

    def populate (self):
        fp = open (os.path.join (os.path.dirname (__file__), "test_data.json"))
        for line in fp:
            j = json.loads (line, object_hook = pymongo.json_util.object_hook)
            self.coll.insert (j)


    def _mr (self, map_js, out):
        self.coll.map_reduce (map_js,
                              "function (k, vals) { var sum = { count: 0 }; for (var i in vals) sum.count += vals[i].count; return sum; }",
                              out = self.cache + 'mr.' + out,
                              finalize = "function (who, res) { res.stamp = new Date(); return res; }")

    def do_mapreduce (self):
        self._mr ("function () { emit(this.%s, { count: 1 }); }" % self.columnizer.get_program_field (), "programs")
        self._mr ("function () { emit(this.%s, { count: 1 }); }" % self.columnizer.get_host_field (), "hosts")
        self._mr ("function () { d = new Date (this.%s*1000); d.setMinutes(0); d.setSeconds(0); emit(d.valueOf()/1000, { count: 1 }); }" % self.columnizer.get_date_field (),
                  "time")

    def tearDown (self):
        self.db[TestConfig.MONGO_DB][self.cache + 'mr.programs'].drop ()
        self.db[TestConfig.MONGO_DB][self.cache + 'mr.hosts'].drop ()
        self.db[TestConfig.MONGO_DB][self.cache + 'mr.time'].drop ()
        self.coll.drop ()
        self.db.disconnect ()
