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
    def test_hosts (self):
        """Test the host statistics"""
        self.populate ()
        self.do_mapreduce ()

        rv = self.app.get ("/stats/hosts/")

        assert "<title>mojology | Statistics</title>" in rv.data
        assert "table.css" not in rv.data
        assert 'host_stats = [{"_id": "localhost", "value": {"count": 32.0, ' in rv.data
        assert '{"_id": "luthien", "value": {"count": 7.0' in rv.data

    def test_programs (self):
        """Test the program statistics"""
        self.populate ()
        self.do_mapreduce ()

        rv = self.app.get ("/stats/programs/")

        assert "<title>mojology | Statistics</title>" in rv.data
        assert 'table.css' not in rv.data
        assert 'prog_stats = [{' in rv.data
        assert '{"_id": "syslog-ng", "value": {"count": 9.0' in rv.data

    def test_time (self):
        """Test the time-based stats"""
        self.populate ()
        self.do_mapreduce ()

        rv = self.app.get ("/stats/time/")

        assert 'table.css' not in rv.data
        assert "<title>mojology | Statistics</title>" in rv.data
        assert 'time_stats = [{' in rv.data
        assert '{"_id": 1294516800.0, "value": {"count": 39.0' in rv.data
