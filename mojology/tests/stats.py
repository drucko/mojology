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

    def test_programs (self):
        """Test the program statistics"""
        self.populate ()

        rv = self.app.get ("/stats/programs/")

        assert 'prog_stats = [{"count": 9.0, "program.name": "syslog-ng"}, {"count": 15.0, "program.name": "sshguard"}, {"count": 1.0, "program.name": "."}, {"count": 10.0, "program.name": "sshd"}, {"count": 1.0, "program.name": "hooman"}, {"count": 2.0, "program.name": "kernel"}, {"count": 1.0, "program.name": "hi"}];' in rv.data
        assert 'table.css' not in rv.data
        assert "<title>mojology | Statistics | Programs</title>" in rv.data

    def test_time (self):
        """Test the time-based stats"""
        self.populate ()

        rv = self.app.get ("/stats/time/")

        assert 'table.css' not in rv.data
        assert "<title>mojology | Statistics | Time</title>" in rv.data
        assert 'time_stats = [{"count": 39.0, "ts": 1294516800.0}];' in rv.data
