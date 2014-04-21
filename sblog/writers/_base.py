import os

from jinja2 import Environment, PackageLoader


class Writer(object):
    """
    Base writer
    """

    dst_folder = None
    _template_env = None


    def __init__(self, app):
        self.app = app
        self.dst_folder = os.path.join(app.cwd, app.dst_folder)

        self.template_env = self.get_template_env()

    def get_template_env(self):
        if self._template_env:
            return self._template_env
        jinja_env = Environment(loader=PackageLoader(package_name='sblog',
                                                     package_path=os.path.join('_themes/', self.app.config['THEME'])))
        self._template_env = jinja_env
        return jinja_env

    def render(self, template_name, **kwargs):
        template = self.get_template_env().get_template(template_name)
        kwargs.update(dict(g=self.app.g))
        return template.render(**kwargs)

    def run(self):
        raise NotImplementedError


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