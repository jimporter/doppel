import os
import platform
import shutil

from .. import *
from doppel import copy, makedirs, mkdir

platform_name = platform.system()


class TestCopy(unittest.TestCase):
    def setUp(self):
        self.stage = os.path.join(test_stage_dir, 'copy')
        if os.path.exists(self.stage):
            shutil.rmtree(self.stage)
        makedirs(self.stage)
        os.chdir(test_data_dir)

        # Git doesn't store empty directories, so make one.
        mkdir('empty_dir', exist_ok=True)

        if platform_name != 'Windows' and not os.path.exists('abssymlink.txt'):
            os.symlink(os.path.abspath('file.txt'), 'abssymlink.txt')

    def test_copy_file(self):
        dst = os.path.join(self.stage, 'file.txt')
        copy('file.txt', dst)
        assertDirectory(self.stage, {
            'file.txt',
        })

    @unittest.skipIf(platform_name == 'Windows', 'permissions fail on Windows')
    def test_copy_file_mode(self):
        dst = os.path.join(self.stage, 'file.txt')
        copy('file.txt', dst, mode=0o600)
        assertDirectory(self.stage, {
            'file.txt',
        })
        self.assertEqual(os.stat(dst).st_mode & 0o777, 0o600)

    def test_recopy_file(self):
        dst = os.path.join(self.stage, 'file.txt')
        open(dst, 'w').close()
        copy('file.txt', dst)
        assertDirectory(self.stage, {
            'file.txt',
        })

    @unittest.skipIf(platform_name == 'Windows', 'permissions fail on Windows')
    def test_recopy_file_mode(self):
        dst = os.path.join(self.stage, 'file.txt')
        open(dst, 'w').close()
        copy('file.txt', dst, mode=0o600)
        assertDirectory(self.stage, {
            'file.txt',
        })
        self.assertEqual(os.stat(dst).st_mode & 0o777, 0o600)

    def test_copy_empty_dir(self):
        dst = os.path.join(self.stage, 'empty_dir')
        copy('empty_dir', dst)
        assertDirectory(self.stage, {
            'empty_dir',
        })

    def test_recopy_empty_dir(self):
        dst = os.path.join(self.stage, 'full_dir')
        mkdir(dst)
        open(os.path.join(dst, 'file.txt'), 'w').close()

        copy('empty_dir', dst)
        assertDirectory(self.stage, {
            'full_dir',
            'full_dir/file.txt',
        })

    def test_copy_full_dir(self):
        dst = os.path.join(self.stage, 'full_dir')
        copy('full_dir', dst)
        assertDirectory(self.stage, {
            'full_dir',
        })

    def test_recopy_full_dir(self):
        dst = os.path.join(self.stage, 'full_dir')
        mkdir(dst)
        open(os.path.join(dst, 'existing.txt'), 'w').close()

        copy('full_dir', dst)
        assertDirectory(self.stage, {
            'full_dir',
            'full_dir/existing.txt',
        })

    def test_copy_full_dir_recursive(self):
        dst = os.path.join(self.stage, 'full_dir')
        copy('full_dir', dst, recursive=True)
        assertDirectory(self.stage, {
            'full_dir',
            'full_dir/file.txt',
        })

    def test_recopy_full_dir_recursive(self):
        dst = os.path.join(self.stage, 'full_dir')
        mkdir(dst)
        open(os.path.join(dst, 'existing.txt'), 'w').close()

        copy('full_dir', dst, recursive=True)
        assertDirectory(self.stage, {
            'full_dir',
            'full_dir/existing.txt',
            'full_dir/file.txt',
        })

    @unittest.skipIf(platform_name == 'Windows',
                     '(usually) no symlinks on Windows')
    def test_copy_symlink(self):
        dst = os.path.join(self.stage, 'symlink.txt')
        copy('symlink.txt', dst)
        assertDirectory(self.stage, {
            'symlink.txt',
        })
        self.assertTrue(os.path.islink(dst))

    @unittest.skipIf(platform_name == 'Windows',
                     '(usually) no symlinks on Windows')
    def test_recopy_symlink(self):
        dst = os.path.join(self.stage, 'symlink.txt')
        open(dst, 'w').close()
        copy('symlink.txt', dst)
        assertDirectory(self.stage, {
            'symlink.txt',
        })
        self.assertTrue(os.path.islink(dst))

    @unittest.skipIf(platform_name == 'Windows',
                     '(usually) no symlinks on Windows')
    def test_copy_symlink_as_file(self):
        dst = os.path.join(self.stage, 'symlink.txt')
        copy('symlink.txt', dst, symlink='never')
        assertDirectory(self.stage, {
            'symlink.txt',
        })
        self.assertFalse(os.path.islink(dst))

    @unittest.skipIf(platform_name == 'Windows',
                     '(usually) no symlinks on Windows')
    def test_copy_abs_symlink(self):
        dst = os.path.join(self.stage, 'abssymlink.txt')
        copy('abssymlink.txt', dst, symlink='always')
        assertDirectory(self.stage, {
            'abssymlink.txt',
        })
        self.assertTrue(os.path.islink(dst))

    @unittest.skipIf(platform_name == 'Windows',
                     '(usually) no symlinks on Windows')
    def test_copy_abs_symlink_as_file(self):
        dst = os.path.join(self.stage, 'abssymlink.txt')
        copy('abssymlink.txt', dst)
        assertDirectory(self.stage, {
            'abssymlink.txt',
        })
        self.assertFalse(os.path.islink(dst))
