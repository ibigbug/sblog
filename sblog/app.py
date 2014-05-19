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
    config = None

    debug = ConfigAttribute('DEBUG')

    _logger = None
    logger_name = ConfigAttribute('LOGGER_NAME')

    debug_log_format = (
        '%(levelname)s: %(message)s\n' +
        '-' * 80
    )

    default_config = dict(
        DEBUG=True,
        LOGGER_NAME=None,
        PERM_LINK_STYLE='${year}/${month}/${day}/${file_name}.html',
        SRC_FOLDER='src',
        DST_FOLDER='dst',
        FORCE_MODE=True,
        THEME='default',

        SITE_BLOG_URL='http://127.0.0.1:8000',
        SITE_BLOG_NAME='SBlog Demo',
        SITE_BLOG_VERSION=god.__version__,
        SITE_AUTHOR_NAME='ibigbug',
        SITE_AUTHOR_EMAIL='i@xiaoba.me',

        SITE_DISQUS_ID=None,
        SITE_GOOGLE_ANALYTICS_ID=None,
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
        config = self.config_class(root_path, self.default_config)
        config_file = os.path.join(self.cwd, 'sblog.json')
        if os.path.exists(config_file):
            print('Config file `sblog.json` founded, loading config...')
            config.from_json_file(config_file)
        return config


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
        self.logger.info('Loading readers...')
        from sblog.readers.markdown import MarkDownReader
        mr = MarkDownReader(self)
        self.logger.info('MarkDownReader loaded.')
        self.logger.info('Readers loading finished.')
        mr.run()
        self.logger.info('Running MarkDownReader.')
        self.logger.info('All readers finished.')

    def _load_writers(self):
        self.logger.info('Loading writers...')
        from sblog.writers import IndexWriter
        self.logger.info('IndexWriter loaded.')
        from sblog.writers import PostWriter
        self.logger.info('PostWriter loaded.')
        from sblog.writers import MetaWriter
        self.logger.info('MetaWriter loaded.')
        from sblog.writers import TagWriter
        self.logger.info('TagWriter loaded.')
        from sblog.writers import FeedWriter
        self.logger.info('FeedWriter loaded.')

        mw = MetaWriter(self)
        self.logger.info('Running MetaWriter.')
        mw.run()
        tw = TagWriter(self)
        self.logger.info('Running TagWriter.')
        tw.run()
        iw = IndexWriter(self)
        self.logger.info('Running IndexWriter.')
        iw.run()
        pw = PostWriter(self)
        self.logger.info('Running PostWriter.')
        pw.run()
        fw = FeedWriter(self)
        self.logger.info('Running FeedWriter.')
        fw.run()