from __future__ import absolute_import
import os
import argparse
from sblog.app import SBlog


cwd = os.getcwd()
app = SBlog(cwd=cwd)
parser = argparse.ArgumentParser(description='Sblog Command Line Interface.')
parser.add_argument('-b', '--build', help='Build a new environment using default configurations.',
                    action='store_true')

if __name__ == '__main__':
    args = parser.parse_args()
    if args.build:
        app.build_env()
    else:
        app.run()


