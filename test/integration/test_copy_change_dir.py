import os
import subprocess
import shutil
import tarfile

from .. import *
from doppel import makedirs


class TestCopyChangeDir(unittest.TestCase):
    def setUp(self):
        self.stage = os.path.join(test_stage_dir, 'copy_change_dir')
        if os.path.exists(self.stage):
            shutil.rmtree(self.stage)
        makedirs(self.stage)
        os.chdir(test_data_dir)

    def test_copy(self):
        subprocess.check_call(['doppel', '-irC', '..', 'data/full_dir',
                               self.stage])
        assertDirectory(self.stage, {
            'full_dir',
            'full_dir/file.txt',
        })

    def test_copy_full_name(self):
        subprocess.check_call(['doppel', '-irNC', '..', 'data/full_dir',
                               self.stage])
        assertDirectory(self.stage, {
            'data',
            'data/full_dir',
            'data/full_dir/file.txt',
        })

    def test_archive(self):
        dst = os.path.join(self.stage, 'archive.tar.gz')
        subprocess.check_call(['doppel', '-irC', '..', '-f', 'gzip',
                               'data/full_dir', dst])
        with tarfile.open(dst) as t:
            self.assertEqual(set(t.getnames()), {
                'full_dir',
                'full_dir/file.txt',
            })

    def test_archive_full_name(self):
        dst = os.path.join(self.stage, 'archive.tar.gz')
        subprocess.check_call(['doppel', '-irNC', '..', '-f', 'gzip',
                               'data/full_dir', dst])
        with tarfile.open(dst) as t:
            self.assertEqual(set(t.getnames()), {
                'data/full_dir',
                'data/full_dir/file.txt',
            })
