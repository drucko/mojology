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

from flask import Flask, g, current_app, redirect, abort, render_template
import pymongo
import datetime

from mojology.utils import templated
from mojology.views.browser import browser
from mojology.views.stats import statsm

def Mojology (config_file = None, config_object = None):
    app = Flask (__name__)
    app.config.from_object ("mojology.default_config")
    app.config.from_envvar ("MOJOLOGY_SETTINGS", True)

    if config_file:
        app.config.from_pyfile (config_file)
    if config_object:
        app.config.from_object (config_object)

    app.register_module (browser)
    app.register_module (statsm, url_prefix = "/stats")

    def version ():
        try:
            import os
            from dulwich.repo import Repo

            repo = Repo (os.path.join (os.path.dirname (__file__), ".."))

            return repo.refs['refs/heads/master']
        except:
            return None
    
    @app.template_filter ('datetime')
    def datetimeformat (value, format='%Y-%m-%d %H:%M:%S'):
        return datetime.datetime.fromtimestamp (float (value)).strftime (format)

    @app.before_request
    def connect_mongo ():
        try:
            g.mongo = pymongo.Connection (current_app.config['MONGO_HOST'], current_app.config['MONGO_PORT'])
        except pymongo.errors.ConnectionFailure, e:
            abort (503)
        g.db = g.mongo[current_app.config['MONGO_DB']]
        g.coll = g.db[current_app.config['MONGO_COLLECTION']]
        if not g.coll:
            abort (503)
        g.pagesize = current_app.config['MOJOLOGY_PAGESIZE']
        g.self_prefix = current_app.config['MOJOLOGY_COLLECTION_PREFIX']
        g.layout = current_app.config['MOJOLOGY_LAYOUT']
        g.mojology_version = version ()
        current_app.disconnected = False

    @app.after_request
    def disconnect_mongo (response):
        try:
            g.mongo.disconnect ()
        except:
            pass
        return response

    @app.errorhandler (404)
    def handler_404 (error):
        return render_template ('http_error.html', error = error), 404

    @app.errorhandler (500)
    def handler_500 (error):
        return render_template ('http_error.html', error = error), 500

    @app.errorhandler (503)
    def handler_503 (error):
        return render_template ('http_error.html', error = error), 503
    
    @app.route ("/about")
    @app.route ("/about/")
    @templated ()
    def about ():
        return None

    @app.route ("/")
    def dashboard ():
        redirect (url_for ("browser.index"))

    return app
