#!/usr/bin/env python
# -*- coding:utf8 -*-

import re
import os
import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter


def render(ns, NameSpace):
    raw_posts = os.listdir(ns.site.content)
    os.chdir(ns.site.content)
    for post in raw_posts:
        print 'reading %s' % post
        container = NameSpace()
        container.meta = NameSpace()

        raw_post = open(post).read().decode('utf-8')
        meta_pattern = re.compile(r'\[meta\].*?\[\/meta\]', re.S)
        metas = meta_pattern.findall(raw_post)[0].split('\n')
        #get meta
        for meta in metas:
            try:
                key, value = meta.split(':')
                container.meta[key.strip()] = value.strip()
            except:
                pass
        #folder meta
        if container.meta.get('folder', None):
            ns.context.folder.append(container.meta.folder)
        container.meta.link = os.path.splitext(post)[0] + '.html'
        #tag meta
        try:
            container.meta.tags = container.meta.tags.split(',')
        except AttributeError:
            container.meta.tags = None
        finally:
            if container.meta.tags:
                container.meta.tags = list(set(container.meta.tags))
        #date meta
        year, month, day = container.meta.date.split('-')
        month = month if len(month) == 2 else '0' + month
        day = day if len(day) == 2 else '0' + day
        container.meta.date = '%s-%s-%s' % (year, month, day)
        md = markdown.Markdown(
            safe_mode=False,
            output_format='xhtml',
        )
        raw_content = raw_post.split('[/meta]')[1]
        container.content = md.convert(hilite(raw_content))
        ns.context.posts.append(container)
    ns.context.folder = list(set(ns.context.folder))
    #sort posts
    ns.context.posts.sort(lambda x, y: cmp(y.meta.date, x.meta.date))


def hilite(raw_post):
    #pygments render
    formatter = HtmlFormatter(noclasses=False)
    pyg_pattern = re.compile(r'~~~:(\w+)(.*?)~~~', re.S)

    def repl(m):
        try:
            lexer = get_lexer_by_name(m.group(1))
        except:
            lexer = TextLexer()
        code = highlight(m.group(2), lexer, formatter)
        return code

    return pyg_pattern.sub(repl, raw_post)
