#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import datetime
from jinja2 import Environment, FileSystemLoader


def write(ns):
    #load templates
    print 'loading templates...'
    tpl_dir = os.path.join(ns.root.path, '_templates/%s') % ns.context.theme
    jinja = Environment(
        loader=FileSystemLoader(tpl_dir, encoding='utf-8'),
        autoescape=False,
    )
    jinja.filters['atomdatetime'] = atom_date_time
    index_tpl = jinja.get_template('index.html')
    post_tpl = jinja.get_template('post.html')
    feed_tpl = jinja.get_template('feed.xml')
    #write index.html
    print 'writing index.html'
    index = index_tpl.render(
        site=ns.site,
        context=ns.context,
        public_posts=ns.context.public_posts,
        preview_posts=ns.context.preview_posts,
        hilite=u'home',
    )
    desti = os.path.join(ns.site.deploy, 'index.html')
    f = open(desti, 'w')
    f.write(index.encode('utf-8'))
    f.close()
    #writer feed.xml
    feed = feed_tpl.render(
        site=ns.site,
        public_posts=ns.context.public_posts,
        preview_posts=ns.context.preview_posts,
        now=datetime.datetime.now()
    )
    desti = os.path.join(ns.site.deploy, 'feed.xml')
    f = open(desti, 'w')
    f.write(feed.encode('utf-8'))
    f.close()

    #write all posts
    for post in ns.context.public_posts:
        print 'writing %s' % post.meta.link
        result = post_tpl.render(
            site=ns.site,
            context=ns.context,
            post=post,
            hilite='home')
        desti = os.path.join(ns.site.deploy, post.meta.link)
        f = open(desti, 'w')
        f.write(result.encode('utf-8'))
        f.close()

        #make folder
        if post.meta.folder:
            folder = os.path.join(ns.site.deploy, post.meta.folder)
            if not os.path.exists(folder):
                print 'making folder %s...' % folder
                os.mkdir(folder)
        else:
            print '%s "folder" key missing...' % post.meta.link
    #deploy folder
    folder_list = list(set(ns.context.folder))
    for f in folder_list:
        folded_posts = []
        print 'deploying folder %s...' % f
        for post in ns.context.public_posts:
            if post.meta.folder == f:
                folded_posts.append(post)
        result = index_tpl.render(
            site=ns.site,
            context=ns.context,
            public_posts=folded_posts,
            hilite=f
        )
        desti_folder = os.path.join(ns.site.deploy, f)
        index = os.path.join(desti_folder, 'index.html')
        f = open(index, 'w')
        f.write(result.encode('utf-8'))
        f.close()


def atom_date_time(value, format='%Y-%m-%dT%H:%M:%SZ'):
    if isinstance(value, datetime.datetime):
        return value.strftime(format)
    year, month, day = value.split('-')
    value = datetime.datetime.now().replace(
        year=int(year),
        month=int(month),
        day=int(day)
    ).strftime(format)
