from setuptools import setup, find_packages
from sblog import __version__ as version


setup(
    name='SBlog',
    version=version,
    author='Yuwei Ba',
    author_email='xiaobayuwei@gmail.com',
    url='blog.xiaoba.me',

    packages=find_packages(),

    keywords=('SBlog', 'markdown', 'Static Blog'),
    description='A simple static blog generator.',
    long_description=open('README.mkd').read(),
    license='MIT License',

    entry_points={
        'console_scripts': ['sblog = sblog.bin:main']
    },
    install_requires=[
        'Jinja2',
        'Pygments',
        'mistune'
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ]

)
