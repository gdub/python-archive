# -*- coding: utf-8 -*-
import os
import shutil
import tempfile
import unittest
from os.path import isfile, join as pathjoin

from archive.compat import IS_PY2
from archive import Archive, extract, UnsafeArchive, UnrecognizedArchiveFormat


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TempDirMixin(object):
    """
    Mixin class for TestCase subclasses to set up and tear down a temporary
    directory for unpacking archives during tests.
    """

    def setUp(self):
        """
        Create temporary directory for testing extraction.
        """
        self.tmpdir = tempfile.mkdtemp()
        # Always start off in TEST_DIR.
        os.chdir(TEST_DIR)

    def tearDown(self):
        """
        Clean up temporary directory.
        """
        shutil.rmtree(self.tmpdir)

    def check_files(self, tmpdir):
        self.assertTrue(isfile(pathjoin(tmpdir, '1')))
        self.assertTrue(isfile(pathjoin(tmpdir, '2')))
        self.assertTrue(isfile(pathjoin(tmpdir, 'foo', '1')))
        self.assertTrue(isfile(pathjoin(tmpdir, 'foo', '2')))
        self.assertTrue(isfile(pathjoin(tmpdir, 'foo', 'bar', '1')))
        self.assertTrue(isfile(pathjoin(tmpdir, 'foo', 'bar', '2')))


class MiscTests(TempDirMixin, unittest.TestCase):

    def test_Archive_instantiation_unrecognized_ext(self):
        f = pathjoin(TEST_DIR, 'files', 'bad', 'unrecognized.txt')
        self.assertRaises(UnrecognizedArchiveFormat, Archive, f)

    def test_extract_method_insecure(self):
        """
        Tests that the insecure extract method indeed unpacks absolute paths
        outside the target directory.
        """
        f = pathjoin('files', 'bad', 'absolute.tar.gz')
        Archive(f).extract(self.tmpdir, method='insecure')
        self.check_files('/tmp')


class ArchiveTester(TempDirMixin):
    """
    A mixin class to be used for testing many Archive methods for a single
    archive file.
    """

    archive = None
    ext = ''

    def setUp(self):
        super(ArchiveTester, self).setUp()
        self.archive_path = pathjoin(TEST_DIR, 'files', self.archive)

    def test_extract_method(self):
        Archive(self.archive_path, ext=self.ext).extract(self.tmpdir)
        self.check_files(self.tmpdir)

    def test_extract_method_fileobject(self):
        f = open(self.archive_path, 'rb')
        Archive(f, ext=self.ext).extract(self.tmpdir)
        self.check_files(self.tmpdir)

    def test_extract_method_no_to_path(self):
        os.chdir(self.tmpdir)
        Archive(self.archive_path, ext=self.ext).extract()
        self.check_files(self.tmpdir)

    def test_extract_method_invalid_method(self):
        self.assertRaises(ValueError,
                          Archive(self.archive_path, ext=self.ext).extract,
                          (self.tmpdir,), {'method': 'foobar'})

    def test_extract_function(self):
        extract(self.archive_path, self.tmpdir, ext=self.ext)
        self.check_files(self.tmpdir)

    def test_extract_function_fileobject(self):
        f = open(self.archive_path, 'rb')
        extract(f, self.tmpdir, ext=self.ext)
        self.check_files(self.tmpdir)

    def test_extract_function_bad_fileobject(self):
        class File:
            pass
        f = File()
        self.assertRaises(UnrecognizedArchiveFormat, extract,
                          (f, self.tmpdir), {'ext': self.ext})

    def test_extract_function_no_to_path(self):
        os.chdir(self.tmpdir)
        extract(self.archive_path, ext=self.ext)
        self.check_files(self.tmpdir)


class TestZip(ArchiveTester, unittest.TestCase):
    archive = 'foobar.zip'


class TestTar(ArchiveTester, unittest.TestCase):
    archive = 'foobar.tar'


class TestGzipTar(ArchiveTester, unittest.TestCase):
    archive = 'foobar.tar.gz'


class TestBzip2Tar(ArchiveTester, unittest.TestCase):
    archive = 'foobar.tar.bz2'


class TestNonAsciiNamedTar(ArchiveTester, unittest.TestCase):
    archive = '圧縮.tgz'


if IS_PY2:
    _UNICODE_NAME = unicode('圧縮.zip', 'utf-8')
else:
    _UNICODE_NAME = '圧縮.zip'


class TestUnicodeNamedZip(ArchiveTester, unittest.TestCase):
    archive = _UNICODE_NAME


class TestExplicitExt(ArchiveTester, unittest.TestCase):
    archive = 'foobar_tar_gz'
    ext = '.tar.gz'


# Archives that have files outside the target directory.

class UnsafeArchiveTester(ArchiveTester):
    """
    Test archives that contain files with destinations outside of the target
    directory, e.g. use absolute paths or relative paths that go up in sthe
    directory hierarchy.
    """

    def test_extract_method(self):
        parent = super(UnsafeArchiveTester, self)
        self.assertRaises(UnsafeArchive, parent.test_extract_method)

    def test_extract_method_fileobject(self):
        parent = super(UnsafeArchiveTester, self)
        self.assertRaises(UnsafeArchive, parent.test_extract_method_fileobject)

    def test_extract_method_no_to_path(self):
        parent = super(UnsafeArchiveTester, self)
        self.assertRaises(UnsafeArchive, parent.test_extract_method_no_to_path)

    def test_extract_function(self):
        parent = super(UnsafeArchiveTester, self)
        self.assertRaises(UnsafeArchive, parent.test_extract_function)

    def test_extract_function_fileobject(self):
        parent = super(UnsafeArchiveTester, self)
        self.assertRaises(UnsafeArchive,
                          parent.test_extract_function_fileobject)

    def test_extract_function_no_to_path(self):
        parent = super(UnsafeArchiveTester, self)
        self.assertRaises(UnsafeArchive,
                          parent.test_extract_function_no_to_path)


class TestOutsideRelative(UnsafeArchiveTester, unittest.TestCase):
    """An archive that goes outside the destination using relative paths."""
    archive = pathjoin('bad', 'relative.tar.gz')


class TestOutsideAbsolute(UnsafeArchiveTester, unittest.TestCase):
    """An archive that goes outside the destination using absolute paths."""
    archive = pathjoin('bad', 'absolute.tar.gz')
