import os


class Writer(object):
    """
    Base writer
    """

    dst_folder = None


    def __init__(self, app):
        self.app = app
        self.dst_folder = os.path.join(app.cwd, app.dst_folder)

    def run(self):
        raise NotImplementedError