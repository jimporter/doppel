import os
import shutil
import subprocess
import tarfile
import zipfile

from .. import *
from doppel import makedirs, mkdir


class TestArchive(unittest.TestCase):
    def setUp(self):
        self.stage = os.path.join(test_stage_dir, 'archive')
        if os.path.exists(self.stage):
            shutil.rmtree(self.stage)
        makedirs(self.stage)
        os.chdir(test_data_dir)

        # Git doesn't store empty directories, so make one.
        mkdir('empty_dir', exist_ok=True)

    def test_archive_file(self):
        dst = os.path.join(self.stage, 'archive.tar.gz')
        subprocess.check_call(['doppel', '-fgzip', 'file.txt', dst])
        with tarfile.open(dst) as t:
            self.assertEqual(set(t.getnames()), {'file.txt'})

    def test_archive_file_mode(self):
        dst = os.path.join(self.stage, 'archive.tar.gz')
        subprocess.check_call(['doppel', '-fgzip', '-m600', 'file.txt', dst])
        with tarfile.open(dst) as t:
            self.assertEqual(set(t.getnames()), {'file.txt'})
            self.assertEqual(t.getmember('file.txt').mode, 0o600)

    def test_archive_empty_dir(self):
        dst = os.path.join(self.stage, 'archive.tar.gz')
        subprocess.check_call(['doppel', '-fgzip', 'empty_dir', dst])
        with tarfile.open(dst) as t:
            self.assertEqual(set(t.getnames()), {'empty_dir'})

    def test_archive_full_dir(self):
        dst = os.path.join(self.stage, 'archive.tar.gz')
        subprocess.check_call(['doppel', '-fgzip', 'full_dir', dst])
        with tarfile.open(dst) as t:
            self.assertEqual(set(t.getnames()), {'full_dir'})

    def test_archive_full_dir_recursive(self):
        dst = os.path.join(self.stage, 'archive.tar.gz')
        subprocess.check_call(['doppel', '-fgzip', '-r', 'full_dir', dst])
        with tarfile.open(dst) as t:
            self.assertEqual(set(t.getnames()), {
                'full_dir',
                'full_dir/file.txt',
            })

    def test_archive_multiple(self):
        dst = os.path.join(self.stage, 'archive.tar.gz')
        subprocess.check_call(['doppel', '-fgzip', '-r', 'empty_dir',
                               'full_dir', 'file.txt', dst])
        with tarfile.open(dst) as t:
            self.assertEqual(set(t.getnames()), {
                'empty_dir',
                'full_dir',
                'full_dir/file.txt',
                'file.txt',
            })

    def test_archive_mutiple_tar(self):
        dst = os.path.join(self.stage, 'archive.tar.gz')
        subprocess.check_call(['doppel', '-ftar', '-r', 'empty_dir',
                               'full_dir', 'file.txt', dst])
        with tarfile.open(dst) as t:
            self.assertEqual(set(t.getnames()), {
                'empty_dir',
                'full_dir',
                'full_dir/file.txt',
                'file.txt',
            })

    def test_archive_mutiple_bzip2(self):
        dst = os.path.join(self.stage, 'archive.tar.gz')
        subprocess.check_call(['doppel', '-fbzip2', '-r', 'empty_dir',
                               'full_dir', 'file.txt', dst])
        with tarfile.open(dst) as t:
            self.assertEqual(set(t.getnames()), {
                'empty_dir',
                'full_dir',
                'full_dir/file.txt',
                'file.txt',
            })

    def test_archive_multiple_zip(self):
        dst = os.path.join(self.stage, 'archive.tar.gz')
        subprocess.check_call(['doppel', '-fzip', '-r', 'empty_dir',
                               'full_dir', 'file.txt', dst])
        with zipfile.ZipFile(dst) as t:
            self.assertEqual(set(t.namelist()), {
                'empty_dir/',
                'full_dir/',
                'full_dir/file.txt',
                'file.txt',
            })

    def test_archive_prefix(self):
        dst = os.path.join(self.stage, 'archive.tar.gz')
        subprocess.check_call(['doppel', '-fgzip', '-r', '--dest-prefix',
                               'prefix', 'empty_dir', 'full_dir', 'file.txt',
                               dst])
        with tarfile.open(dst) as t:
            self.assertEqual(set(t.getnames()), {
                'prefix/empty_dir',
                'prefix/full_dir',
                'prefix/full_dir/file.txt',
                'prefix/file.txt',
            })
