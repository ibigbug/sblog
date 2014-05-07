import os
import random


root_path = os.path.join('/tmp', 'sblog_test_env')
try:
    os.mkdir(root_path)
except OSError as e:
    pass
cwd = root_path

from sblog.app import SBlog

app = None

def make_env():
    global app
    app = SBlog(cwd=cwd)
    app.debug = True
    app.build_env()

def gene_src():
    post_content = (
        '# title%d\n'
        '* date: 2014-01-01\n'
        '* tags: asdf,asdf,adsf\n'
        '\n'
        'content'
    )

    profile_content = (
        '* twitter: ibigbug\n'
        '* weibo: ibigbug\n'
        '\n'
        'GOGOGOG'
    )

    about_content = (
        '* Powered by SBlog\n'
    )

    src_files = ['post1.mkd', 'post2.mkd', 'sub1/post3.mkd', 'sub2/depth2/depth3/depth4/post4.mkd']
    for f in src_files:
        f = os.path.join(app.cwd, app.src_folder, f)
        sub_dir = os.path.dirname(f)
        if not os.path.isdir(sub_dir):
            os.makedirs(sub_dir)
        with open(f, 'wb') as src_file:
            src_file.write(post_content % random.randint(1,100000000))

    with open(os.path.join(app.cwd, app.src_folder, '_about.mkd'), 'wb') as fd:
        fd.write(about_content)
    with open(os.path.join(app.cwd, app.src_folder, '_profile.mkd'), 'wb') as fd:
        fd.write(profile_content)


def reader_test():
    from sblog.readers.markdown import MarkDownReader
    reader = MarkDownReader(app)
    reader.run()


def writer_test():
    from sblog.writers.index import IndexWriter
    from sblog.writers.post import PostWriter
    from sblog.writers.meta import MetaWriter
    from sblog.writers.tag import TagWriter

    mw = MetaWriter(app)
    mw.run()
    tw = TagWriter(app)
    tw.run()
    iw = IndexWriter(app)
    iw.run()
    pw = PostWriter(app)
    pw.run()



def clean():
    import shutil
    shutil.rmtree(app.cwd)


if __name__ == '__main__':
    make_env()
    gene_src()
    reader_test()
    writer_test()
    #clean()
