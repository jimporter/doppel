import os
import subprocess
import shutil

from .. import *
from doppel import makedirs


class TestCopyParents(unittest.TestCase):
    def setUp(self):
        self.stage = os.path.join(test_stage_dir, 'copy_parents')
        if os.path.exists(self.stage):
            shutil.rmtree(self.stage)
        makedirs(self.stage)
        os.chdir(test_data_dir)

    def test_parents_only(self):
        dst = os.path.join(self.stage, 'dir', 'subdir')
        subprocess.check_call(['doppel', '-p', dst])
        assertDirectory(self.stage, {
            'dir',
            'dir/subdir',
        })

    def test_parents_onto(self):
        dst = os.path.join(self.stage, 'dir', 'file.txt')
        subprocess.check_call(['doppel', '-p', 'file.txt', dst])
        assertDirectory(self.stage, {
            'dir',
            'dir/file.txt',
        })

    def test_parents_into(self):
        dst = os.path.join(self.stage, 'dir', 'subdir')
        subprocess.check_call(['doppel', '-ip', 'file.txt', dst])
        assertDirectory(self.stage, {
            'dir',
            'dir/subdir',
            'dir/subdir/file.txt',
        })
