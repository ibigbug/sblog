#!/usr/bin/env python
# -*- coding:utf8 -*-

import re
import markdown
from sblog.namespace import NameSpace


def render(post):
    container = NameSpace()
    container.meta = NameSpace()
    raw_post = open(post).read()
    pattern = re.compile(r'\[meta\].*?\[\/meta\]', re.S)
    metas = pattern.findall(raw_post)[0].split('\n')
    for meta in metas:
        try:
            key, value = meta.split(':')
            container.meta[key] = value
        except:
            pass
    md = markdown.Markdown(
        safe_mode='escape',
        output_format='xhtml',
    )
    raw_content = raw_post.split('[/meta]')[1]
    container.content = md.convert(raw_content)
    print container.content
    return container
