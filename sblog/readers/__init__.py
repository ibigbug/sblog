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
        #pygments render
        formatter = HtmlFormatter(noclasses=False)
        pyg_pattern = re.compile(r'\[code:(\w+)\](.*?)\[\/code\]', re.S)
        m = re.search(pyg_pattern, raw_post)
        if m:
            try:
                lexer = get_lexer_by_name(m.group(1))
            except:
                lexer = TextLexer()
            code = highlight(m.group(2), lexer, formatter)
            code = code.replace('\n', '<br />')
            raw_post = pyg_pattern.sub(code, raw_post).decode('utf-8')
        mkd_pattern = re.compile(r'\[meta\].*?\[\/meta\]', re.S)
        metas = mkd_pattern.findall(raw_post)[0].split('\n')
        #get meta
        for meta in metas:
            try:
                key, value = meta.split(':')
                container.meta[key] = value.strip()
            except:
                pass
        if hasattr(container.meta, 'folder') and container.meta.folder != None:
            ns.context.folder.append(container.meta.folder)
        container.meta.link = os.path.splitext(post)[0] + '.html'
        try:
            container.meta.tags = container.meta.tags.split(',')
        except AttributeError:
            container.meta.tags = None
        md = markdown.Markdown(
            safe_mode=False,
            output_format='xhtml',
        )
        raw_content = raw_post.split('[/meta]')[1]
        container.content = md.convert(raw_content)
        ns.context.posts.append(container)
    ns.context.folder = list(set(ns.context.folder))
