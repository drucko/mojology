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
import os, sys
from werkzeug.wsgi import DispatcherMiddleware

if len (sys.argv) > 1:
    cfg_file = os.path.realpath (sys.argv[1])
    if not os.path.exists (cfg_file):
        cfg_file = None
else:
    cfg_file = os.path.realpath (os.path.join (os.path.dirname (__file__), "local_settings.py"))
    if not os.path.exists (cfg_file):
        cfg_file = None

app = Mojology (config_file = cfg_file)
sites = {}

for site in sys.argv[2:]:
    sapp = Mojology (config_file = os.path.realpath (site))
    if not "MOJOLOGY_SITE_ROOT" in sapp.config:
        raise SyntaxError, "'%s' does not set MOJOLOGY_SITE_ROOT" % site
    sites[sapp.config['MOJOLOGY_SITE_ROOT']] = sapp.wsgi_app

app.wsgi_app = DispatcherMiddleware (app.wsgi_app, sites)
app.run ()
