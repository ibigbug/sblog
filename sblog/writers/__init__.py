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
        f.write(result.encode('utf-8'))
        f.close()

        #write folder
        folder = os.path.join(ns.root.deploy, (post.meta.folder).strip())
        if not os.path.exists(folder):
            print 'making folder %s...' % folder
            os.mkdir(folder)
        ns.folder.append((post.meta.folder).strip())
    #deploy folder
    tpl = jinja.get_template('index.html')
    folder_list = list(set(ns.folder))
    for f in folder_list:
        posts = []
        print 'deploying folder %s...' % f
        for post in ns.context:
            if (post.meta.folder).strip() == f:
                posts.append(post)
        result = tpl.render(site=ns.site,context=posts)
        desti_folder = os.path.join(path, f)
        index = os.path.join(desti_folder, 'index.html')
        f = open(index, 'w')
        f.write(result)
        f.close()
