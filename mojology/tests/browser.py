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

class BrowserTest (mojology.tests.TestCase):
    def test_empty_db (self):
        """Test that the initial test collection is empty"""
        rv = self.app.get ("/")
        # Empty DB test is incomplete
        pass

    def test_simple_data (self):
        """Test that importing our data worked"""
        self.populate ()
        rv = self.app.get ("/")
        assert "<header><h2>Logs</h2></header>" in rv.data
        assert "Latest log messages, page #" in rv.data
        assert '<span id="page_counter">1</span>' in rv.data
        assert '<span id="maxpage">4</span>' in rv.data

    def test_index_pagination (self):
        """Test index pagination"""
        self.populate ()
        rv = self.app.get ("/page/2")
        assert '<span id="page_counter">2</span>' in rv.data
        assert '<a href="/log/4d28cb30f310ef4f0000001c" class="hidden">[35486.147294] warning: `VirtualBox&#39; uses 32-bit capabilities (legacy support ...</a>' in rv.data

    def test_index_pagination_oob (self):
        """Test index pagination, out of bounds cases"""
        self.populate ()

        rv = self.app.get ("/page/0")
        assert rv.status_code == 404

        rv = self.app.get ("/page/5")
        assert rv.status_code == 404

    def test_host_filter (self):
        """Test the host filtering"""
        self.populate ()

        rv = self.app.get ("/host/luthien/")
        assert "<title>mojology | Logs</title>" in rv.data
        assert "Latest log messagesfor luthien" in rv.data
        assert '<span id="page_counter">1</span>' in rv.data
        assert '<span id="maxpage">1</span>' in rv.data

    def test_host_filter_pagination (self):
        """Test the pagination with host filtering"""
        self.populate ()

        rv = self.app.get ("/host/localhost/page/3")
        assert "<title>mojology | Logs</title>" in rv.data
        assert "Latest log messagesfor localhost" in rv.data
        assert '<span id="page_counter">3</span>' in rv.data
        assert '<span id="maxpage">4</span>' in rv.data

    def test_host_filter_pagination_oob (self):
        """Test the pagination with host filtering, with out of bounds range"""
        self.populate ()

        rv = self.app.get ("/host/luthien/page/0")
        assert rv.status_code == 404

        rv = self.app.get ("/host/luthien/page/42")
        assert rv.status_code == 404

    def test_host_invalid_filter (self):
        """Test the host filtering with an invalid host"""
        self.populate ()

        rv = self.app.get ("/host/does.not.exist/")
        assert rv.status_code == 404

    def test_log (self):
        """Test the log details page"""
        self.populate ()

        rv = self.app.get ("/log/4d28cd01f310ef4f00000024")

        assert "<title>mojology | Logs" in rv.data
        assert "<h3>Log message #4d28cd01f310ef4f00000024</h3>" in rv.data
        assert "Hello world! This concludes our demo session." in rv.data
        assert "0xdeadbeef" in rv.data

    def test_log_invalid_oid (self):
        """Test the log details with an invalid OID"""
        self.populate ()

        rv = self.app.get ("/log/invalid")
        assert rv.status_code == 404

    def test_log_not_found (self):
        """Test the log details with a non-existing, but valid OID"""
        self.populate ()

        rv = self.app.get ("/log/fd28cd01f310ef4f00000024")
        assert rv.status_code == 404

    def test_log_dyn (self):
        """Test the stripped down log details"""
        self.populate ()

        rv = self.app.get ("/log/4d28cd01f310ef4f00000024/dyn")
        assert "<title>" not in rv.data
        assert "Hello world! This concludes our demo session." not in rv.data
        assert "0xdeadbeef" in rv.data

    def test_log_dyn_message (self):
        """Test the stripped down log details, with an extra message box"""
        self.populate ()

        rv = self.app.get ("/log/4d28cb1cf310ef4f0000001b/dyn")
        assert "<title>" not in rv.data
        assert '<table id="message">' in rv.data
        assert "dst.mongodb" in rv.data
        assert "<th>classifier</th>" in rv.data
