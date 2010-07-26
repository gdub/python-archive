from distutils.core import setup

setup(
    name = 'python-archive',
    version = '0.1',
    author = 'Gary Wilson Jr.',
    author_email = 'gary.wilson@gmail.com',
    packages = ['archive', 'archive.test'],
    url = 'http://code.google.com/p/python-archive/',
    license = 'LICENSE.txt',
    description = ('Simple library that provides a common interface for'
                   ' extracting zip and tar archives.'),
    long_description = open('README.txt').read(),
)
