import json
import imp

from ._compat import string_types
from .utils import import_string


class ConfigAttribute(object):
    def __init__(self, name, get_converter=None):
        self.__name__ = name
        self.get_converter = get_converter

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        rv = obj.config[self.__name__]
        if self.get_converter is not None:
            rv = self.get_converter(rv)
        return rv

    def __set__(self, obj, value):
        obj.config[self.__name__] = value


class Config(dict):
    def __init__(self, root_path, default_config=None):
        self.root_path = root_path
        self.update(default_config)

    def __getattr__(self, item):
        return self.get(item, None)

    def __setattr__(self, key, value):
        self[key] = value

    def from_json_file(self, file_path):
        try:
            with open(file_path) as json_file:
                obj = json.loads(json_file.read())
        except IOError as e:
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise

        for key in obj.keys():
            self[key] = obj[key]

        return True

    def from_pyfile(self, file_path):
        d = imp.new_module('config')
        d.__file__ = file_path
        try:
            with open(file_path) as config_file:
                exec(compile(config_file.read(), file_path, 'exec'), d.__dict__)
        except IOError as e:
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        self.from_object(d)
        return True

    def from_object(self, obj):
        if isinstance(obj, string_types):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = obj[key]

    def get_namespace(self, namespace, lowercase=True):
        rv = {}
        for k, v in self.iteritems():
            if not k.startswith(namespace):
                continue
            key = k[len(namespace):]
            if lowercase:
                key = key.lower()
            rv[key] = v
        return rv