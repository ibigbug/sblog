from __future__ import print_function
import os
import argparse

from sblog import __version__ as version
from sblog import __author__ as author
from sblog.app import SBlog


cwd = os.getcwd()
app = SBlog(cwd=cwd)
parser = argparse.ArgumentParser(description='Sblog Command Line Interface.')
parser.add_argument('-b', '--build', help='Build a new environment using default configurations.',
                    action='store_true')
parser.add_argument('-v', '--version', help='Print SBlog version.',
                    action='store_true')


def print_version():
    print('SBlog, version: %s' % version)
    print(author)


def main():
    args = parser.parse_args()
    if args.build:
        app.build_env()
    if args.version:
        print_version()
    else:
        app.run()


if __name__ == '__main__':
    main()


