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
import unittest
import pymongo, pymongo.json_util
import json
import os

class TestConfig (object):
    DEBUG = True
    TESTING = True
    MONGO_HOST = "127.0.0.1"
    MONGO_PORT = 27017
    MONGO_DB = "demo"
    MONGO_COLLECTION = "messages"
    MONGO_DYNVARS = "dyn"

    MOJOLOGY_PAGESIZE = 10

class TestCase (unittest.TestCase):
    def setUp (self):
        self.mojology = Mojology (config_object = "mojology.tests.TestConfig")
        self.app = self.mojology.test_client ()

        self.db = pymongo.Connection (TestConfig.MONGO_HOST, TestConfig.MONGO_PORT)
        self.coll = self.db[TestConfig.MONGO_DB][TestConfig.MONGO_COLLECTION]
        self.pagesize = TestConfig.MOJOLOGY_PAGESIZE
        self.dyn_vars = TestConfig.MONGO_DYNVARS

        self.coll.drop ()

    def populate (self):
        fp = open (os.path.join (os.path.dirname (__file__), "test_data.json"))
        for line in fp:
            j = json.loads (line, object_hook = pymongo.json_util.object_hook)
            self.coll.insert (j)

    def tearDown (self):
        self.coll.drop ()
        self.db.disconnect ()
