#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import shutil

from sblog import __version__ as version
from namespace import ns
import readers
import writers
import config


def init():
    ns.root.path = os.path.dirname(__file__)
    ns.root.template_dir = os.path.join(os.path.dirname(__file__),
                                        '_templates')
    ns.root.version = version
    ns.site.site_name = config.site_name
    ns.site.author = config.author


def build():
    if 'config.py' in os.listdir('.'):
        read()
        write()
    else:
        s = raw_input("build an environment?(y/n):")
        if s != 'n':
            shutil.copyfile(os.path.join(ns.root.path, 'config.py'),
                            'config.py')
            shutil.copytree(os.path.join(ns.root.path, '_static'), '_static')
            shutil.copytree(os.path.join(ns.root.path, '_templates'),
                            '_templates')
            os.mkdir('content')
            os.mkdir('deploy')
            print 'build finished'
            return


def read():
    print 'reading...'
    for dirpath, dirnames, raw_posts in os.walk('content'):
        for p in raw_posts:
            post = readers.render(os.path.join(dirpath, p))
            post.filename = os.path.splitext(p)[0] + '.html'
            ns.context.append(post)
    return


def write():
    print 'writing...'
    for post in ns.context:
        path = os.path.join(ns.root.deploy, post.filename + '')
        writers.write(path, post, ns)


def main():
    init()
    build()

if __name__ == '__main__':
    main()
