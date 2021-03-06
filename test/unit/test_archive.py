import os
import platform
import shutil
import tarfile

from .. import *
from doppel import archive, makedirs, mkdir

platform_name = platform.system()


class BaseTestArchive:
    def setUp(self):
        self.stage = os.path.join(test_stage_dir, 'archive')
        self.archive = os.path.join(self.stage, 'archive{}'.format(self.ext))
        if os.path.exists(self.stage):
            shutil.rmtree(self.stage)
        makedirs(self.stage)
        os.chdir(test_data_dir)

        # Git doesn't store empty directories, so make one.
        mkdir('empty_dir', exist_ok=True)

        if platform_name != 'Windows' and not os.path.exists('abssymlink.txt'):
            os.symlink(os.path.abspath('file.txt'), 'abssymlink.txt')

    def test_file(self):
        with archive.open(self.archive, 'w', self.format) as f:
            f.add('file.txt')
        self.assertContents(self.archive, {
            'file.txt',
        })

    def test_empty_dir(self):
        with archive.open(self.archive, 'w', self.format) as f:
            f.add('empty_dir')
        self.assertContents(self.archive, {
            'empty_dir/',
        })

    def test_full_dir(self):
        with archive.open(self.archive, 'w', self.format) as f:
            f.add('full_dir')
        self.assertContents(self.archive, {
            'full_dir/',
            'full_dir/file.txt',
        })

    def test_full_dir_nonrecursive(self):
        with archive.open(self.archive, 'w', self.format) as f:
            f.add('full_dir', recursive=False)
        self.assertContents(self.archive, {
            'full_dir/',
        })

    def test_file_arcname(self):
        with archive.open(self.archive, 'w', self.format) as f:
            f.add('file.txt', 'archived.txt')
        self.assertContents(self.archive, {
            'archived.txt',
        })

    def test_file_mode(self):
        with archive.open(self.archive, 'w', self.format) as f:
            f.add('file.txt', mode=0o600)
        self.assertContents(self.archive, {
            'file.txt',
        })
        self.assertMode(self.archive, 'file.txt', 0o600)

    @unittest.skipIf(platform_name == 'Windows',
                     '(usually) no symlinks on Windows')
    def test_symlink(self):
        with archive.open(self.archive, 'w', self.format) as f:
            f.add('symlink.txt', 'link.txt')
        self.assertContents(self.archive, {
            'link.txt',
        })
        self.assertType(self.archive, 'link.txt', tarfile.SYMTYPE)

    @unittest.skipIf(platform_name == 'Windows',
                     '(usually) no symlinks on Windows')
    def test_symlink_as_file(self):
        with archive.open(self.archive, 'w', self.format) as f:
            f.add('symlink.txt', 'link.txt', symlink='never')
        self.assertContents(self.archive, {
            'link.txt',
        })
        self.assertType(self.archive, 'link.txt', tarfile.REGTYPE)

    @unittest.skipIf(platform_name == 'Windows',
                     '(usually) no symlinks on Windows')
    def test_abs_symlink(self):
        with archive.open(self.archive, 'w', self.format) as f:
            f.add('abssymlink.txt', 'link.txt', symlink='always')
        self.assertContents(self.archive, {
            'link.txt',
        })
        self.assertType(self.archive, 'link.txt', tarfile.SYMTYPE)

    @unittest.skipIf(platform_name == 'Windows',
                     '(usually) no symlinks on Windows')
    def test_abs_symlink_as_file(self):
        with archive.open(self.archive, 'w', self.format) as f:
            f.add('abssymlink.txt', 'link.txt')
        self.assertContents(self.archive, {
            'link.txt',
        })
        self.assertType(self.archive, 'link.txt', tarfile.REGTYPE)


class TestZip(BaseTestArchive, unittest.TestCase):
    format = 'zip'
    ext = '.zip'

    def assertContents(self, filename, contents):
        with archive.open(filename, 'r', self.format) as f:
            self.assertEqual(set(f.namelist()), set(contents))

    def assertMode(self, filename, member, mode):
        pass

    def assertType(self, filename, member, type):
        pass


class TestTar(BaseTestArchive, unittest.TestCase):
    format = 'tar'
    ext = '.tar'

    def assertContents(self, filename, contents):
        with archive.open(filename, 'r', self.format) as f:
            self.assertEqual(set(f.getnames()),
                             {i.rstrip('/') for i in contents})

    def assertMode(self, filename, member, mode):
        with archive.open(filename, 'r', self.format) as f:
            self.assertEqual(f.getmember(member).mode, mode)

    def assertType(self, filename, member, type):
        with archive.open(filename, 'r', self.format) as f:
            self.assertEqual(f.getmember(member).type, type)


class TestGzip(TestTar, unittest.TestCase):
    format = 'gzip'
    ext = '.tar.gz'


class TestBzip2(TestTar, unittest.TestCase):
    format = 'bzip2'
    ext = '.tar.bz2'
