import json


class Post(object):
    """Post model"""
    marked = None  # result parsed by mistune.markdown(file_content)
    title = None
    meta = dict()
    body = None

    perm_link = None

    __fields__ = ('meta', 'body')

    def __init__(self, fields_dict=None):
        if fields_dict is not None:
            for key, value in fields_dict.iteritems():
                setattr(self, key, value)

    def set_meta(self, meta):
        self.meta = meta

    def get_meta(self):
        return self.meta

    def set_body(self, body):
        self.body = body

    def get_body(self):
        return self.body

    def set_perm_link(self, link):
        self.perm_link = link

    def get_perm_link(self):
        return self.perm_link

    def __repr__(self):
        return '''
            meta: %s
            body: %s
            perm_link: %s
        ''' % (json.dumps(self.meta), self.body, self.perm_link)