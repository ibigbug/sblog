import os
from ._base import Writer


class IndexWriter(Writer):
    template_name = 'index.html'

    def run(self):
        index_path = os.path.join(self.dst_folder, 'index.html')
        with open(index_path, 'wb') as f:
            f.write(self.render(self.template_name, rv=self.prepare_posts()))

    def prepare_posts(self):
        rv = {}
        all_years = self.get_all_year()
        for year in all_years:
            rv[str(year)] = self.get_post_by_year(year)
        return rv