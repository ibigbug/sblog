#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
install_requires = ['markdown', 'Jinja2']


from sblog import __version__ as version

setup(
    name='sblog',
    version=version,
    author='xiaoba',
    author_email='xiaobayuwei@gmail.com',
    url='http://blog.xiaoba.me',
    packages=['sblog', 'sblog.writers', 'sblog.readers'],
    description='A lightweight static weblog generator',
    long_description=open('README.mkd').read(),
    license='BSD License',
    entry_points={
        'console_scripts': ['sblog= sblog.main:main'],
    },
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Programming Language :: Python',
    ]
)
