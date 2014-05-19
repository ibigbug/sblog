import os
import datetime

from ._base import Writer


class FeedWriter(Writer):
    template_name = 'feed.xml'

    def run(self):
        file_path = os.path.join(self.dst_folder, self.template_name)
        with open(file_path, 'wb') as f:
            f.write(self.render(self.template_name,
                    posts=self.app.posts,
                    now=datetime.datetime.utcnow()
                    ))
