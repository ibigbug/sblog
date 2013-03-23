#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import shutil

from sblog import __version__ as version
from namespace import ns, NameSpace
from utils import timer
import readers
import writers
import ConfigParser



def init():
    print 'Sblog version %s' % version
    ns.root.path = os.path.dirname(__file__)
    ns.root.version = version
    ns.root.template_dir = os.path.join(os.path.dirname(__file__),
                                        '_templates')
    ns.root.static_dir = os.path.join(os.path.dirname(__file__), '_static')
    ns.site.proj_dir = os.getcwd()


def pre_read():
    cf = ConfigParser.ConfigParser()
    config = os.path.join(ns.site.proj_dir, 'config.ini')
    cf.read(config)

    ns.site.site_name = cf.get('basic', 'site_name').decode('utf-8')
    ns.site.author = cf.get('basic', 'author').decode('utf-8')
    ns.site.site_url = cf.get('basic', 'site_url').decode('utf-8')
    ns.site.content = os.path.join(os.getcwd(), 'content')
    ns.site.deploy = os.path.join(os.getcwd(), 'deploy')
    try:
        ns.context.ga = cf.get('extra', 'ga')
    except:
        ns.context.ga = None
    try:
        ns.context.disqus = cf.get('extra', 'disqus')
    except:
        ns.context.disqus = None
    try:
        ns.context.theme = cf.get('extra','theme')
    except:
        ns.context.theme = 'default'


def build():
    if 'config.ini' in os.listdir('.'):
        pre_read()
        read()
        write()
        gene_static()
    else:
        s = raw_input("build an environment?(y/n):")
        if s != 'n':
            shutil.copyfile(os.path.join(ns.root.path, 'config.ini'),
                            'config.ini')
            os.mkdir('content')
            os.mkdir('deploy')
            print 'build finished'
            return


def read():
    print 'reading...'
    readers.render(ns, NameSpace)


def write():
    print 'writing...'
    writers.write(ns)


def gene_static():
    desti_static = os.path.join(ns.site.deploy, 'static')
    if os.path.exists(desti_static):
        print 'removing old static files...'
        shutil.rmtree(desti_static)
    print 'generating new static files...'
    shutil.copytree(ns.root.static_dir, desti_static)

@timer()
def main():
    init()
    build()

if __name__ == '__main__':
    main()
