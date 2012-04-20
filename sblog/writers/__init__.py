#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
from jinja2 import Environment, FileSystemLoader



def write(ns):
    tpl_dir = os.path.join(ns.root.path, '_templates')
    jinja = Environment(
        loader=FileSystemLoader(tpl_dir),
        autoescape=False,
    )
    #write index.html
    print 'writing index.html'
    index_tpl = jinja.get_template('index.html')
    post_tpl = jinja.get_template('post.html')
    result = index_tpl.render(site=ns.site, context=ns.context,
                              posts=ns.context.posts, hilite='home')
    desti = os.path.join(ns.site.deploy, 'index.html')
    f = open(desti, 'w')
    f.write(result)
    f.close()
    #write post.html
    for post in ns.context.posts:
        print 'writing %s' % post.meta.link
        result = post_tpl.render(site=ns.site, context=ns.context,
                                 post=post, hilite='home')
        desti = os.path.join(ns.site.deploy, post.meta.link)
        f = open(desti, 'w')
        f.write(result.encode('utf-8'))
        f.close()

        #write folder
        folder = os.path.join(ns.site.deploy, post.meta.folder)
        if not os.path.exists(folder):
            print 'making folder %s...' % folder
            os.mkdir(folder)
    #deploy folder
    folder_list = list(set(ns.context.folder))
    for f in folder_list:
        folded_posts = []
        print 'deploying folder %s...' % f
        for post in ns.context.posts:
            if post.meta.folder == f:
                folded_posts.append(post)
        result = index_tpl.render(site=ns.site, context=ns.context,
                                  posts=folded_posts, hilite=f)
        desti_folder = os.path.join(ns.site.deploy, f)
        index = os.path.join(desti_folder, 'index.html')
        f = open(index, 'w')
        f.write(result)
        f.close()
