import os
from ._base import Writer
from mistune import markdown


class MetaWriter(Writer):
    templates = dict(about='_about.mkd', profile='_profile.mkd')

    def run(self):
        for key, value in self.templates.iteritems():
            file_path = os.path.join(self.app.cwd, self.app.src_folder, value)
            with open(file_path, 'rb') as f:
                content = f.read()
                self.app.g[key] = markdown(content)
