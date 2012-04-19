#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
from jinja2 import Environment, FileSystemLoader


def write(path, context, ns):
    jinja = Environment(
        loader=FileSystemLoader('_templates'),
        autoescape=False,
    )
    tpl =  jinja.get_template('index.html')
    print context
    resutl = tpl.render(context=context)
    f = open(path, 'w')
    f.write(resutl)
    f.close()
