#!/usr/bin/env python
# -*- coding:utf8 -*-

import functools
import datetime


class timer(object):
    def __call__(self, method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            start = datetime.datetime.now()
            print 'start at %s...' % start
            method(*args, **kwargs)
            end = datetime.datetime.now()
            print 'finish at %s...' % end
            #print 'using %s...' % (end - start).seconds
            print 'using %s...' % (end - start)
        return wrapper
