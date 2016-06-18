import os
import shutil

from .. import *
from doppel import copy, makedirs, mkdir


class TestCopy(unittest.TestCase):
    def setUp(self):
        self.stage = os.path.join(test_stage_dir, 'copy')
        if os.path.exists(self.stage):
            shutil.rmtree(os.path.join(self.stage))
        makedirs(self.stage)
        os.chdir(test_data_dir)

        # Git doesn't store empty directories, so make one.
        mkdir('empty_dir', exist_ok=True)

    def test_copy_file(self):
        dst = os.path.join(self.stage, 'file.txt')
        copy('file.txt', dst)
        assertDirectory(self.stage, {
            'file.txt',
        })

    def test_recopy_file(self):
        dst = os.path.join(self.stage, 'file.txt')
        open(dst, 'w').close()
        copy('file.txt', dst)
        assertDirectory(self.stage, {
            'file.txt',
        })

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
