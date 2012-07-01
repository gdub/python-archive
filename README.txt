==============
python-archive
==============

This package provides a simple, pure-Python interface for handling various
archive file formats.  Currently, archive extraction is the only supported
action.  Supported file formats include:

* Zip formats and equivalents: ``.zip``, ``.egg``, ``.jar``.
* Tar and compressed tar formats: ``.tar``, ``.tar.gz``, ``.tgz``,
  ``.tar.bz2``, ``.tz2``.


Example usage
=============

Using the ``Archive`` class::

    from archive import Archive

    a = Archive('files.tar.gz')
    a.extract()

Using the ``extract`` convenience function::

    from archive import extract
    # Extract in current directory.
    extract('files.tar.gz')
    # Extract in directory 'unpack_dir'.
    extract('files.tar.gz', 'unpack_dir')

More examples
-------------
Passing a file-like object is also supported::

    f = open('files.tar.gz', 'rb')
    Archive(f).extract()

If a file does not have the correct extension, or is not recognized correctly,
you may try explicitly specifying an extension (with leading period)::

    Archive('files.wrongext', ext='.tar.gz').extract()
    # or
    extract('files.wrongext', ext='.tar.gz')


Similar tools
=============

* http://pypi.python.org/pypi/patool/ - portable command line archive file
  manager.
* http://pypi.python.org/pypi/gocept.download/ - zc.buildout recipe for
  downloading and extracting an archive.
