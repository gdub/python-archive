import os
import shutil
import tempfile
import unittest

from archive import Archive, extract


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class ArchiveTester(object):
    archive = None

    def setUp(self):
        """
        Create temporary directory for testing extraction.
        """
        self.tmpdir = tempfile.mkdtemp()
        self.archive_path = os.path.join(TEST_DIR, self.archive)
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
        self.assertTrue(os.path.isfile(os.path.join(self.tmpdir, '1')))
        self.assertTrue(os.path.isfile(os.path.join(self.tmpdir, '2')))
        self.assertTrue(os.path.isfile(os.path.join(self.tmpdir, 'foo', '1')))
        self.assertTrue(os.path.isfile(os.path.join(self.tmpdir, 'foo', '2')))
        self.assertTrue(os.path.isfile(os.path.join(self.tmpdir, 'foo', 'bar', '1')))
        self.assertTrue(os.path.isfile(os.path.join(self.tmpdir, 'foo', 'bar', '2')))


class TestZip(ArchiveTester, unittest.TestCase):
    archive = 'foobar.zip'


class TestTar(ArchiveTester, unittest.TestCase):
    archive = 'foobar.tar'


class TestGzipTar(ArchiveTester, unittest.TestCase):
    archive = 'foobar.tar.gz'


class TestBzip2Tar(ArchiveTester, unittest.TestCase):
    archive = 'foobar.tar.bz2'
