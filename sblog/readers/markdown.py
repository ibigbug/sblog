import re
import os
import datetime

from ._base import Reader
from .post import Post

import mistune

class MarkDownReader(Reader):
    """
    Parse *.mkd
    """
    __allow_suffix__ = ['.md', '.mkd', '.mdown', '.markdown']

    title_pattern = re.compile(ur'<h1>(.+?)</h1>')
    meta_pattern = re.compile(ur'<li>(.+?)</li>')
    body_pattern = re.compile(ur'<p>.+?$')

    def run(self):
        input_files = filter(lambda f: os.path.splitext(f)[-1] in self.__allow_suffix__, self.input_files)
        for f in input_files:
            parsed = self._parse_content(f)
            p = Post(parsed)
            p.set_perm_link(self.calc_perm_link(p))
            self.app.posts.append(p)

    def _parse_content(self, file_path):
        fd = open(file_path, 'rb')
        file_content = fd.read().decode('utf-8')
        fd.close()

        marked = mistune.markdown(file_content)
        try:
            title = self.title_pattern.findall(marked)[0]
            meta = self.meta_pattern.findall(marked)
            body = self.body_pattern.findall(marked)[0]
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
            body=body,
            marked=marked
        )

    @staticmethod
    def _parse_date(s):
        date = datetime.datetime.strptime(s, '%Y-%m-%d')
        return date