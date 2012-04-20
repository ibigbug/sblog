#!/usr/bin/env python
# -*- coding:utf8 -*-


class NameSpace(dict):
    def __getattr__(self, key):
        if key in self:
            return self[key]
    def __setattr__(self, key, value):
        self[key] = value
    def __delattr__(self, key):
        try:
            del self[key]
        except:
            raise AttributeError


ns = NameSpace()
ns.root = NameSpace()
ns.root.content = 'content'
ns.root.deploy = 'deploy'
ns.site = NameSpace()
ns.context = []
ns.folder = []
