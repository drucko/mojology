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

class DefaultLayout:
    msg = None
    headers = None
    fields = None
    sort_on = None
    keys = None

    def _get_key (self, key):
        if key in self.msg:
            return self.msg[key]
        else:
            return ""

    def __init__ (self, *args, **kwargs):
        self.setup (*args, **kwargs)

    def setup (self, msg = None):
        if msg:
            self.set_msg (msg)

        self.headers = [
            {
                'name': 'Date',
                'path': 'DATE',
                'is_date': True
            },
            {
                'name': 'Host',
                'path': 'HOST',
                'is_host': True,
            },
            {
                'name': 'Facility & Level',
                'path': ['FACILITY', '.', 'PRIORITY']
            },
            {
                'name': 'Program',
                'path': 'PROGRAM',
            },
            {
                'name': 'Message',
                'path': 'MESSAGE',
                'is_message': True,
            }
        ]
    
        self.fields = dict (date = 'DATE',
                            host = 'HOST',
                            program = 'PROGRAM',
                            message = 'MESSAGE'
                           )
        self.sort_on = 'DATE'
            
    def set_msg (self, msg):
        self.msg = msg
        for h in self.headers:
            if type (h['path']) == list:
                h['value'] = ""
                for p in h['path']:
                    if p in self.msg:
                        h['value'] += self.msg[p]
                    else:
                        h['value'] += p
            else:
                h['value'] = self._get_key (h['path'])
                
        if self._get_key ('PID') != "":
            self.headers[3]['value'] += '[' + self._get_key ('PID') + ']'

        self.keys = dict ()
        for key in self.msg:
            if key not in ['DATE', 'HOST', 'FACILITY', 'PRIORITY', 'PROGRAM',
                           'PID', 'MESSAGE', '_id']:
                if key.upper () == key:
                    name = key.capitalize ()
                else:
                    name = key
                self.keys[name] = self.msg[key]

        return ""

class OldLayout:
    msg = None
    headers = None
    fields = None
    sort_on = None
    keys = None

    def _get_key (self, key):
        if key in self.msg:
            return self.msg[key]
        else:
            try:
                key.index ('.')
            except:
                return ""
            (p, c) = key.split ('.')
            if (p in self.msg) and (c in self.msg[p]):
                return self.msg[p][c]
            return ""

    def __init__ (self, *args, **kwargs):
        self.setup (*args, **kwargs)

    def setup (self, msg = None):
        if msg:
            self.set_msg (msg)

        self.headers = [
            {
                'name': 'Date',
                'path': 'ts',
                'is_date': True
            },
            {
                'name': 'Host',
                'path': 'host',
                'is_host': True,
            },
            {
                'name': 'Facility & Level',
                'path': ['log.facility', '.', 'log.level']
            },
            {
                'name': 'Program',
                'path': 'program.name',
            },
            {
                'name': 'Message',
                'path': 'message',
                'is_message': True,
            }
        ]
    
        self.fields = dict (date = 'ts',
                            host = 'host',
                            program = 'program.name',
                            message = 'message'
                           )
        self.sort_on = 'ts'
            
    def set_msg (self, msg):
        self.msg = msg
        for h in self.headers:
            if type (h['path']) == list:
                h['value'] = ""
                for p in h['path']:
                    if self._get_key (p) != "":
                        h['value'] += self._get_key (p)
                    else:
                        h['value'] += p
            else:
                h['value'] = self._get_key (h['path'])
                
        if self._get_key ('program.pid') != "":
            self.headers[3]['value'] += '[' + self._get_key ('program.pid') + ']'

        self.keys = dict ()
        for key in self.msg['dyn']:
            if key.upper () == key:
                name = key.capitalize ()
            else:
                name = key
            self.keys[name] = self.msg['dyn'][key]

        return ""
