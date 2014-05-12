import re
import os
import datetime

from ._base import Reader
from .post import Post

import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter


class MyRenderer(mistune.Renderer):
    def block_code(self, code, lang=None):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except:
            lexer = get_lexer_by_name('javascript', stripall=True)
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)


class MarkDownReader(Reader):
    """
    Parse *.mkd
    """
    renderer = MyRenderer()
    md = mistune.Markdown(renderer)

    __allow_suffix__ = ['.md', '.mkd', '.mdown', '.markdown']

    title_pattern = re.compile(ur'<h1>(.+?)</h1>')
    meta_pattern = re.compile(ur'<li>(.+?)</li>', re.M)

    def run(self):
        input_files = filter(lambda f: (os.path.splitext(f)[-1] in self.__allow_suffix__) and
                                       (not os.path.basename(f).startswith('_')),
                             self.input_files)

        for f in input_files:
            parsed = self._parse_content(f)
            p = Post(parsed)
            p.set_perm_link(self.calc_perm_link(p))
            self.app.posts.append(p)

    def _parse_content(self, file_path):
        fd = open(file_path, 'rb')

        header = ''
        body = ''
        recording = True

        for line in fd:
            if recording and line.startswith('---'):
                recording = False
            elif recording:
                header += line.decode('utf-8')
            else:
                body += line.decode('utf-8')
        fd.close()
        header = mistune.markdown(header)
        body = self.md.render(body)

        try:
            title = self.title_pattern.findall(header)[0]
            meta = self.meta_pattern.findall(header)

        except:
            from ._base import MarkDownReaderException
            e = MarkDownReaderException('Post parse exception on file: %s' % file_path)
            raise e

        meta_dict = dict(title=title)
        for m in meta:
            try:
                key, value = m.split(':', 2)  # only * key: value will be saved as Post attribute
                if key == 'date':
                    date = self._parse_date(value.strip())
                    meta_dict['year'] = date.year
                    meta_dict['month'] = date.month
                    meta_dict['day'] = date.day
                meta_dict[key.strip()] = value.strip()
            except:
                pass
        return dict(
            meta=meta_dict,
            body=body
        )

    @staticmethod
    def _parse_date(s):
        date = datetime.datetime.strptime(s, '%Y-%m-%d')
        return date


