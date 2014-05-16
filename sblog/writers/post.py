import os
from ._base import Writer
from ._base import PostExistsException


class PostWriter(Writer):

    posts = []
    template_name = 'post.html'

    def run(self):
        self.posts = self.app.posts
        self.write()

    def write(self):
        for p in self.posts:
            perm_link = p.get_perm_link()
            file_path = os.path.join(self.dst_folder, perm_link)

            file_dir = os.path.dirname(file_path)
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir, mode=0755)
            if os.path.exists(file_path):
                self.logger.info('Post `%s` exists.' % file_path)
                continue

            with open(file_path, 'wb') as fd:
                fd.write(self.render(self.template_name, post=p))