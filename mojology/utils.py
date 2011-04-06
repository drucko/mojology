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

from functools import wraps
from flask import request, render_template, g, current_app, abort
import pymongo

def templated(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint \
                    .replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator

def connected():
    def decorator (cf):
        @wraps(cf)
        def decorated_function (*args, **kwargs):
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
            g.mojology_version = current_app.version
            r = cf (*args, **kwargs)
            g.mongo.disconnect ()
            return r

        return decorated_function
    return decorator
