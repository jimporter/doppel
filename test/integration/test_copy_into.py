import os
import platform
import shutil
import subprocess

from .. import *
from doppel import makedirs, mkdir

platform_name = platform.system()


class TestCopyInto(unittest.TestCase):
    def setUp(self):
        self.stage = os.path.join(test_stage_dir, 'copy_into')
        if os.path.exists(self.stage):
            shutil.rmtree(os.path.join(self.stage))
        makedirs(self.stage)
        os.chdir(test_data_dir)

        # Git doesn't store empty directories, so make one.
        mkdir('empty_dir', exist_ok=True)

    def test_copy_file(self):
        subprocess.check_call(['doppel', '-i', 'file.txt', self.stage])
        assertDirectory(self.stage, {
            'file.txt',
        })

    @unittest.skipIf(platform_name == 'Windows', 'permissions fail on Windows')
    def test_copy_file_mode(self):
        subprocess.check_call(['doppel', '-im600', 'file.txt', self.stage])
        assertDirectory(self.stage, {
            'file.txt',
        })
        stat = os.stat(os.path.join(self.stage, 'file.txt'))
        self.assertEqual(stat.st_mode & 0o777, 0o600)

    def test_recopy_file(self):
        open(os.path.join(self.stage, 'file.txt'), 'w').close()
        subprocess.check_call(['doppel', '-i', 'file.txt', self.stage])
        assertDirectory(self.stage, {
            'file.txt',
        })

    @unittest.skipIf(platform_name == 'Windows', 'permissions fail on Windows')
    def test_recopy_file_mode(self):
        open(os.path.join(self.stage, 'file.txt'), 'w').close()
        subprocess.check_call(['doppel', '-im600', 'file.txt', self.stage])
        assertDirectory(self.stage, {
            'file.txt',
        })
        stat = os.stat(os.path.join(self.stage, 'file.txt'))
        self.assertEqual(stat.st_mode & 0o777, 0o600)

    def test_copy_empty_dir(self):
        subprocess.check_call(['doppel', '-i', 'empty_dir', self.stage])
        self.assertEqual(set(os.listdir(self.stage)), {'empty_dir'})
        assertDirectory(self.stage, {
            'empty_dir',
        })

    def test_recopy_empty_dir(self):
        dst = os.path.join(self.stage, 'empty_dir')
        mkdir(dst)
        open(os.path.join(dst, 'file.txt'), 'w').close()

        subprocess.check_call(['doppel', '-i', 'empty_dir', self.stage])
        assertDirectory(self.stage, {
            'empty_dir',
            'empty_dir/file.txt',
        })

    def test_copy_full_dir(self):
        subprocess.check_call(['doppel', '-i', 'full_dir', self.stage])
        assertDirectory(self.stage, {
            'full_dir',
        })

    def test_recopy_full_dir(self):
        dst = os.path.join(self.stage, 'full_dir')
        mkdir(dst)
        open(os.path.join(dst, 'existing.txt'), 'w').close()

        subprocess.check_call(['doppel', 'full_dir', self.stage])
        assertDirectory(self.stage, {
            'full_dir',
            'full_dir/existing.txt',
        })

    def test_copy_full_dir_recursive(self):
        subprocess.check_call(['doppel', '-ir', 'full_dir', self.stage])
        assertDirectory(self.stage, {
            'full_dir',
            'full_dir/file.txt',
        })

    def test_recopy_full_dir_recursive(self):
        dst = os.path.join(self.stage, 'full_dir')
        mkdir(dst)
        open(os.path.join(dst, 'existing.txt'), 'w').close()

        subprocess.check_call(['doppel', '-ir', 'full_dir', self.stage])
        assertDirectory(self.stage, {
            'full_dir',
            'full_dir/existing.txt',
            'full_dir/file.txt',
        })

    def test_copy_multiple(self):
        subprocess.check_call(['doppel', '-r', 'empty_dir', 'full_dir',
                               'file.txt', self.stage])
        assertDirectory(self.stage, {
            'file.txt',
            'empty_dir',
            'full_dir',
            'full_dir/file.txt',
        })

    def test_copy_full_name(self):
        subprocess.check_call(['doppel', '-iN', 'file.txt',
                               'full_dir/file.txt', self.stage])
        assertDirectory(self.stage, {
            'file.txt',
            'full_dir',
            'full_dir/file.txt',
        })
