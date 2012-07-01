import os
import sys
import tarfile
import zipfile

from archive.compat import IS_PY2, is_string


class ArchiveException(Exception):
    """Base exception class for all archive errors."""

class UnrecognizedArchiveFormat(ArchiveException):
    """Error raised when passed file is not a recognized archive format."""


def extract(path, to_path='', ext=''):
    """
    Unpack the tar or zip file at the specified path to the directory
    specified by to_path.
    """
    Archive(path, ext=ext).extract(to_path)


class Archive(object):
    """
    The external API class that encapsulates an archive implementation.
    """

    def __init__(self, file, ext=''):
        """
        Arguments:
        * 'file' can be a string path to a file or a file-like object.
        * Optional 'ext' argument can be given to override the file-type
          guess that is normally performed using the file extension of the
          given 'file'.  Should start with a dot, e.g. '.tar.gz'.
        """
        self._archive = self._archive_cls(file, ext=ext)(file)

    @staticmethod
    def _archive_cls(file, ext=''):
        """
        Return the proper Archive implementation class, based on the file type.
        """
        cls = None
        filename = None
        if is_string(file):
            filename = file
        else:
            try:
                filename = file.name
            except AttributeError:
                raise UnrecognizedArchiveFormat(
                    "File object not a recognized archive format.")
        lookup_filename = filename + ext
        base, tail_ext = os.path.splitext(lookup_filename.lower())
        cls = extension_map.get(tail_ext)
        if not cls:
            base, ext = os.path.splitext(base)
            cls = extension_map.get(ext)
        if not cls:
            raise UnrecognizedArchiveFormat(
                "Path not a recognized archive format: %s" % filename)
        return cls

    def extract(self, to_path=''):
        self._archive.extract(to_path)

    def list(self):
        self._archive.list()


class BaseArchive(object):
    """
    Base Archive class.  Implementations should inherit this class.
    """
    def __del__(self):
        if hasattr(self, "_archive"):
            self._archive.close()

    def extract(self):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError


class TarArchive(BaseArchive):

    def __init__(self, file):
        # tarfile's open uses different parameters for file path vs. file obj.
        if is_string(file):
            self._archive = tarfile.open(name=file)
        else:
            self._archive = tarfile.open(fileobj=file)

    def list(self, *args, **kwargs):
        self._archive.list(*args, **kwargs)

    def extract(self, to_path):
        self._archive.extractall(to_path)


class ZipArchive(BaseArchive):

    def __init__(self, file):
        # ZipFile's 'file' parameter can be path (string) or file-like obj.
        self._archive = zipfile.ZipFile(file)

    def list(self, *args, **kwargs):
        self._archive.printdir(*args, **kwargs)

    def extract(self, to_path):
        self._archive.extractall(to_path)


extension_map = {
    '.egg': ZipArchive,
    '.jar': ZipArchive,
    '.tar': TarArchive,
    '.tar.bz2': TarArchive,
    '.tar.gz': TarArchive,
    '.tgz': TarArchive,
    '.tz2': TarArchive,
    '.zip': ZipArchive,
}
