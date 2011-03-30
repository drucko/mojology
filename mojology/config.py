class Columnizer:
    def _get_key (self, msg, key):
        if key in msg:
            return msg[key]
        else:
            return ""

    def get_date_field (self):
        return 'DATE'

    def get_host_field (self):
        return 'HOST'

    def get_program_field (self):
        return 'PROGRAM'

    def get_date (self, msg):
        return self._get_key (msg, 'DATE')

    def get_host (self, msg):
        return self._get_key (msg, 'HOST')

    def get_facility (self, msg):
        return self._get_key (msg, 'FACILITY')

    def get_level (self, msg):
        return self._get_key (msg, 'PRIORITY')

    def get_program (self, msg):
        return self._get_key (msg, 'PROGRAM')

    def get_pid (self, msg):
        return self._get_key (msg, 'PID')

    def get_message (self, msg):
        return self._get_key (msg, 'MESSAGE')

    def filter_key (self, key):
        if key not in ['DATE', 'HOST', 'FACILITY', 'PRIORITY', 'PROGRAM', 'PID', 'MESSAGE', '_id']:
            return key.capitalize ()
