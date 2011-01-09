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

import mojology.tests

class StatsTest (mojology.tests.TestCase):
    def test_basic (self):
        """Basic stats page test"""
        self.populate ()

        rv = self.app.get ("/stats/")

        assert "<title>mojology | Statistics</title>" in rv.data
        assert "table.css" not in rv.data
        assert 'host_stats = [{"count": 7.0, "host": "luthien"}, {"count": 32.0, "host": "localhost"}];' in rv.data
