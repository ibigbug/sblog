import os

from ._base import Writer


class TagWriter(Writer):
    template_name = 'tag.html'
    tags = []

    def run(self):
        self.tags = self.app.g.tags = self.calc_tags()

        file_path = os.path.join(self.dst_folder, self.template_name)
        with open(file_path, 'wb') as fd:
            fd.write(self.render(self.template_name,
                                 tags=self.tags,
                                 get_post_by_tag=self.get_post_by_tag))

    def calc_tags(self):
        rv = []
        for p in self.app.posts:
            if p.meta.has_key('tags'):
                rv.extend(p.meta.get('tags'))
        return set(rv)

    def get_post_by_tag(self, tag):
        for p in self.app.posts:
            if not p.meta.has_key('tags'):
                continue
            if tag in p.meta.get('tags'):
                yield p