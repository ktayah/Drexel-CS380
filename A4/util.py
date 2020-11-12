import re
import sys


class Arguments:

    def __init__(self):
        self.args = {}
        for arg in sys.argv[1:]:
            arg = re.sub(r'^-*', '', arg.strip())
            parts = arg.split('=')
            if len(parts) >= 2:
                self.args[parts[0]] = parts[1]

    def get(self, name, default=None):
        return self.args[name] if name in self.args else default

    def get_int(self, name, default=None):
        return int(self.args[name]) if name in self.args else default

    def get_list(self, name, default=None):
        return self.args[name].split(',') if name in self.args else default

    def get_int_list(self, name, default=None):
        return [int(s) for s in self.args[name].split(',')] if name in self.args else default
