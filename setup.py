from distutils.core import setup

setup(
    name = 'python-archive',
    version = '0.2-dev',
    author = 'Gary Wilson Jr.',
    author_email = 'gary.wilson@gmail.com',
    packages = ['archive', 'archive.test'],
    url = 'https://github.com/gdub/python-archive',
    license = 'LICENSE.txt',
    description = ('Simple library that provides a common interface for'
                   ' extracting zip and tar archives.'),
    long_description = open('README.txt').read(),
)
