from __future__ import print_function

import os

import __init__ as god
from .config import Config, ConfigAttribute
from .utils import import_string
from .utils import Global

root_path = os.path.abspath(os.path.dirname(__file__))
cwd = os.getcwd()


class SBlog(object):

    config_class = Config

    debug = ConfigAttribute('DEBUG')

    logger_name = ConfigAttribute('LOGGER_NAME')

    debug_log_format = (
        '-' * 80 + '\n' +
        '%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n' +
        '%(message)s\n' +
        '-' * 80
    )

    default_config = dict(
        DEBUG=False,
        LOGGER_NAME=None,
        PERM_LINK_STYLE='${year}/${month}/${day}/${title}.html',
        SRC_FOLDER='src',
        DST_FOLDER='dst',
        THEME='default',

        SITE_BLOG_URL='http://127.0.0.1:8000',
        SITE_BLOG_NAME='SBlog Demo',
        SITE_BLOG_VERSION=god.__version__,
        SITE_AUTHOR_NAME='ibigbug',
        SITE_AUTHOR_EMAIL='i@xiaoba.me',
    )

    g = Global()

    src_folder = None
    dst_folder = None
    posts = []

    def __init__(self, config_file=None, cwd=cwd):
        self.config_file = config_file
        self.root_path = root_path
        self.cwd = cwd

        self.config = self.make_config()
        self.src_folder = self.config['SRC_FOLDER']
        self.dst_folder = self.config['DST_FOLDER']

        self._logger = None
        self.logger_name = self.__class__.__name__

        self.make_global()

    @property
    def logger(self):
        from .log import create_logger
        if self._logger:
            return self._logger
        self._logger = rv = create_logger(self)
        return rv

    def make_config(self):
        root_path = self.root_path
        return self.config_class(root_path, self.default_config)

    def make_global(self):
        _g = self.config.get_namespace('SITE_')
        self.g.update(_g)

    def build_env(self):
        src_folder = os.path.join(self.cwd, self.src_folder)
        dst_folder = os.path.join(self.cwd, self.dst_folder)

        try:
            os.mkdir(src_folder, 0755)
            os.mkdir(dst_folder, 0755)
        except OSError as e:
            e.strerror = 'Can not build env: %s' % e.strerror
            self.logger.info('Environment already exists.')

    def run(self):
        self._load_readers()
        self._load_writers()
        self.done()

    @staticmethod
    def done():
        msg = 'Done'
        print(msg)

    def _load_readers(self):
        from sblog.readers.markdown import MarkDownReader
        mr = MarkDownReader(self)
        mr.run()

    def _load_writers(self):
        from sblog.writers.index import IndexWriter
        from sblog.writers.post import PostWriter
        from sblog.writers.meta import MetaWriter
        from sblog.writers.tag import TagWriter

        mw = MetaWriter(self)
        mw.run()
        tw = TagWriter(self)
        tw.run()
        iw = IndexWriter(self)
        iw.run()
        pw = PostWriter(self)
        pw.run()