import os
import platform
import subprocess
import shutil

from .. import *
from doppel import makedirs, mkdir

platform_name = platform.system()


class TestCopyOnto(unittest.TestCase):
    def setUp(self):
        self.stage = os.path.join(test_stage_dir, 'copy_onto')
        if os.path.exists(self.stage):
            shutil.rmtree(os.path.join(self.stage))
        makedirs(self.stage)
        os.chdir(test_data_dir)

        # Git doesn't store empty directories, so make one.
        mkdir('empty_dir', exist_ok=True)

    def test_copy_file(self):
        dst = os.path.join(self.stage, 'file.txt')
        subprocess.check_call(['doppel', 'file.txt', dst])
        assertDirectory(self.stage, {
            'file.txt',
        })

    @unittest.skipIf(platform_name == 'Windows', 'permissions fail on Windows')
    def test_copy_file_mode(self):
        dst = os.path.join(self.stage, 'file.txt')
        subprocess.check_call(['doppel', '-m600', 'file.txt', dst])
        assertDirectory(self.stage, {
            'file.txt',
        })
        self.assertEqual(os.stat(dst).st_mode & 0o777, 0o600)

    def test_recopy_file(self):
        dst = os.path.join(self.stage, 'file.txt')
        open(dst, 'w').close()
        subprocess.check_call(['doppel', 'file.txt', dst])
        assertDirectory(self.stage, {
            'file.txt',
        })

    @unittest.skipIf(platform_name == 'Windows', 'permissions fail on Windows')
    def test_recopy_file_mode(self):
        dst = os.path.join(self.stage, 'file.txt')
        open(dst, 'w').close()
        subprocess.check_call(['doppel', '-m600', 'file.txt', dst])
        assertDirectory(self.stage, {
            'file.txt',
        })
        self.assertEqual(os.stat(dst).st_mode & 0o777, 0o600)

    def test_copy_empty_dir(self):
        dst = os.path.join(self.stage, 'empty_dir')
        subprocess.check_call(['doppel', 'empty_dir', dst])
        assertDirectory(self.stage, {
            'empty_dir',
        })

    def test_recopy_empty_dir(self):
        dst = os.path.join(self.stage, 'full_dir')
        mkdir(dst)
        open(os.path.join(dst, 'file.txt'), 'w').close()

        subprocess.check_call(['doppel', 'empty_dir', dst])
        assertDirectory(self.stage, {
            'full_dir',
            'full_dir/file.txt',
        })

    def test_copy_full_dir(self):
        dst = os.path.join(self.stage, 'full_dir')
        subprocess.check_call(['doppel', 'full_dir', dst])
        assertDirectory(self.stage, {
            'full_dir',
        })

    def test_recopy_full_dir(self):
        dst = os.path.join(self.stage, 'full_dir')
        mkdir(dst)
        open(os.path.join(dst, 'existing.txt'), 'w').close()

        subprocess.check_call(['doppel', 'full_dir', dst])
        assertDirectory(self.stage, {
            'full_dir',
            'full_dir/existing.txt',
        })

    def test_copy_full_dir_recursive(self):
        dst = os.path.join(self.stage, 'full_dir')
        subprocess.check_call(['doppel', '-r', 'full_dir', dst])
        assertDirectory(self.stage, {
            'full_dir',
            'full_dir/file.txt',
        })

    def test_recopy_full_dir_recursive(self):
        dst = os.path.join(self.stage, 'full_dir')
        mkdir(dst)
        open(os.path.join(dst, 'existing.txt'), 'w').close()

        subprocess.check_call(['doppel', '-r', 'full_dir', dst])
        assertDirectory(self.stage, {
            'full_dir',
            'full_dir/existing.txt',
            'full_dir/file.txt',
        })
