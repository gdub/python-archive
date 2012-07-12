from distutils.core import setup

VERSION = '0.2'

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Topic :: System :: Archiving',
    'Topic :: System :: Software Distribution',
]

setup(
    name = 'python-archive',
    version = VERSION,
    classifiers = CLASSIFIERS,
    author = 'Gary Wilson Jr.',
    author_email = 'gary@thegarywilson.com',
    packages = ['archive', 'archive.test'],
    url = 'https://github.com/gdub/python-archive',
    license = 'MIT License',
    description = ('Simple library that provides a common interface for'
                   ' extracting zip and tar archives.'),
    long_description = open('README.rst').read(),
    tests_require=["tox", "pytest", "pep8"],
)
