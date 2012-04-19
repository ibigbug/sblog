#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
from jinja2 import Environment, FileSystemLoader


def write(path, ns):
    jinja = Environment(
        loader=FileSystemLoader('_templates'),
        autoescape=False,
    )
    #write index.html
    print 'writing index.html'
    tpl = jinja.get_template('index.html')
    result = tpl.render(site=ns.site, context=ns.context)
    desti = os.path.join(path, 'index.html')
    f = open(desti, 'w')
    f.write(result)
    f.close()
    #write post.html
    tpl = jinja.get_template('post.html')
    for post in ns.context:
        print 'writing %s' % post.meta.link
        result = tpl.render(site=ns.site, post=post)
        desti = os.path.join(path, post.meta.link)
        f = open(desti, 'w')
        f.write(result)
        f.close()
