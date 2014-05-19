import os
from string import Template


class Reader(object):
    """
    meta Reader
    All readers should inherit me
    """
    max_dir_level = 3
    src_folder = None
    input_files = []
    perm_link_style = None

    def __init__(self, app):
        self.app = app
        self.src_folder = os.path.join(app.cwd, app.src_folder)
        self.perm_link_style = app.config.get('PERM_LINK_STYLE')

        self.walk_dir(self.src_folder)

    def walk_dir(self, dir_name, curr_level=0):
        for root, dirs, files in os.walk(dir_name):
            files = map(lambda f: os.path.join(root, f), files)
            self.input_files.extend(files)
            if len(dirs) >= 0:
                if curr_level >= self.max_dir_level:
                    import warnings
                    warnings.warn('Max src folder depth is %d' % self.max_dir_level)
                    return
                else:
                    for d in dirs:
                        curr_level += 1
                        self.walk_dir(d, curr_level)

    def calc_perm_link(self, post):
        t = Template(self.perm_link_style)
        return t.safe_substitute(post.meta)

    def run(self):
        """
        Readers must implement this method
        """
        raise NotImplementedError


class MarkDownReaderException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value