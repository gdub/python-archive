from distutils.core import setup

VERSION = '0.2-dev'

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: System :: Archiving',
    'Topic :: System :: Software Distribution',
]

setup(
    name = 'python-archive',
    version = VERSION,
    classifiers = CLASSIFIERS,
    author = 'Gary Wilson Jr.',
    author_email = 'gary.wilson@gmail.com',
    packages = ['archive', 'archive.test'],
    url = 'https://github.com/gdub/python-archive',
    license = 'MIT License',
    description = ('Simple library that provides a common interface for'
                   ' extracting zip and tar archives.'),
    long_description = open('README.txt').read(),
    tests_require=["tox", "pytest", "pep8"],
)
