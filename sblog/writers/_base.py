import os
import shutil
import datetime

from jinja2 import Environment, PackageLoader


def rfc3339_datetime_format(value):
    formatt = '%Y-%m-%dT%H:%M:%SZ'
    if not isinstance(value, datetime.datetime):
        year, month, day = value.split('-')
        value = datetime.datetime.utcnow().replace(
            year=int(year),
            month=int(month),
            day=int(day)
        )
    return value.strftime(formatt)


class Writer(object):
    """
    Base writer
    """

    dst_folder = None
    _template_env = None


    def __init__(self, app):
        self.app = app
        self.logger = app.logger
        self.dst_folder = os.path.join(app.cwd, app.dst_folder)

        self.template_env = self.get_template_env()

        self._copy_static()

    def get_template_env(self):
        if self._template_env:
            return self._template_env
        jinja_env = Environment(loader=PackageLoader(package_name='sblog',
                                                     package_path=os.path.join('_themes/', self.app.config['THEME'])))
        jinja_env.filters['atomdatetime'] = rfc3339_datetime_format
        self._template_env = jinja_env
        return jinja_env

    def _copy_static(self):
        src = os.path.join(self.app.root_path, '_themes', self.app.config['THEME'], 'static')
        dst = os.path.join(self.app.cwd, self.app.config['DST_FOLDER'], 'static')
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    def render(self, template_name, **kwargs):
        template = self.get_template_env().get_template(template_name)
        kwargs.update(dict(g=self.app.g))
        return template.render(**kwargs).encode('utf-8')

    def run(self):
        raise NotImplementedError

    def get_post_by_year(self, year):
        for p in self.app.posts:
            if p.meta.get('year') == year:
                yield p

    def get_all_year(self):
        rv = []
        for p in self.app.posts:
            year = p.meta.get('year')
            if year in rv:
                continue
            rv.append(year)
        return rv


class ThemeNotFoundException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Theme `%s` not found.' % self.value


class TemplateNotFoundException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Template `%s` not found.' % self.value


class PostExistsException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Post `%s` exists.' % self.value
