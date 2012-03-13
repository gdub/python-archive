# -*- coding: utf-8 -*-
import os
import shutil
import tempfile
import unittest
from os.path import isfile, join as pathjoin

from archive import Archive, IS_PY2, extract

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class ArchiveTester(object):
    archive = None

    def setUp(self):
        """
        Create temporary directory for testing extraction.
        """
        self.tmpdir = tempfile.mkdtemp()
        self.archive_path = pathjoin(TEST_DIR, self.archive)
        # Always start off in TEST_DIR.
        os.chdir(TEST_DIR)

    def tearDown(self):
        """
        Clean up temporary directory.
        """
        shutil.rmtree(self.tmpdir)

    def test_extract_method(self):
        Archive(self.archive).extract(self.tmpdir)
        self.check_files(self.tmpdir)

    def test_extract_method_no_to_path(self):
        os.chdir(self.tmpdir)
        Archive(self.archive_path).extract()
        self.check_files(self.tmpdir)

    def test_extract_function(self):
        extract(self.archive_path, self.tmpdir)
        self.check_files(self.tmpdir)

    def test_extract_function_no_to_path(self):
        os.chdir(self.tmpdir)
        extract(self.archive_path)
        self.check_files(self.tmpdir)

    def check_files(self, tmpdir):
        self.assertTrue(isfile(pathjoin(self.tmpdir, '1')))
        self.assertTrue(isfile(pathjoin(self.tmpdir, '2')))
        self.assertTrue(isfile(pathjoin(self.tmpdir, 'foo', '1')))
        self.assertTrue(isfile(pathjoin(self.tmpdir, 'foo', '2')))
        self.assertTrue(isfile(pathjoin(self.tmpdir, 'foo', 'bar', '1')))
        self.assertTrue(isfile(pathjoin(self.tmpdir, 'foo', 'bar', '2')))


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
