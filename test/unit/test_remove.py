import os
import platform
import shutil

from .. import *
from doppel import makedirs, remove

platform_name = platform.system()


class TestRemove(unittest.TestCase):
    def setUp(self):
        self.stage = os.path.join(test_stage_dir, 'remove')
        if os.path.exists(self.stage):
            shutil.rmtree(self.stage)
        makedirs(self.stage)
        os.chdir(test_data_dir)

    def test_remove(self):
        dst = os.path.join(self.stage, 'file.txt')
        open(dst, 'w').close()
        remove(dst)
        self.assertFalse(os.path.exists(dst))

    def test_remove_dir(self):
        dst = os.path.join(self.stage, 'subdir')
        makedirs(dst)
        self.assertRaises(OSError, remove, dst)
        shutil.rmtree(dst)

    def test_remove_nonexist(self):
        dst = os.path.join(self.stage, 'file.txt')
        self.assertRaises(OSError, remove, dst)
        remove(dst, nonexist_ok=True)
