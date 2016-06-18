import os
import unittest
import subprocess
import shutil

from doppel import makedirs, mkdir

this_dir = os.path.abspath(os.path.dirname(__file__))
test_data_dir = os.path.join(this_dir, '..', 'data')
test_stage_dir = os.path.join(this_dir, '..', 'stage')


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
        self.assertTrue(os.path.isfile(dst))

    def test_recopy_file(self):
        dst = os.path.join(self.stage, 'file.txt')
        open(dst, 'w').close()
        subprocess.check_call(['doppel', 'file.txt', dst])
        self.assertTrue(os.path.isfile(dst))

    def test_copy_empty_dir(self):
        dst = os.path.join(self.stage, 'empty_dir')
        subprocess.check_call(['doppel', 'empty_dir', dst])
        self.assertTrue(os.path.isdir(dst))
        self.assertEqual(os.listdir(dst), [])

    def test_recopy_empty_dir(self):
        dst = os.path.join(self.stage, 'full_dir')
        mkdir(dst)
        open(os.path.join(dst, 'file.txt'), 'w').close()

        subprocess.check_call(['doppel', 'empty_dir', dst])
        self.assertTrue(os.path.isdir(dst))
        self.assertEqual(set(os.listdir(dst)), {'file.txt'})

    def test_copy_full_dir(self):
        dst = os.path.join(self.stage, 'full_dir')
        subprocess.check_call(['doppel', 'full_dir', dst])
        self.assertTrue(os.path.isdir(dst))
        self.assertEqual(os.listdir(dst), [])

    def test_recopy_full_dir(self):
        dst = os.path.join(self.stage, 'full_dir')
        mkdir(dst)
        open(os.path.join(dst, 'existing.txt'), 'w').close()

        subprocess.check_call(['doppel', 'full_dir', dst])
        self.assertTrue(os.path.isdir(dst))
        self.assertEqual(set(os.listdir(dst)), {'existing.txt'})

    def test_copy_full_dir_recursive(self):
        dst = os.path.join(self.stage, 'full_dir')
        subprocess.check_call(['doppel', '-r', 'full_dir', dst])
        self.assertTrue(os.path.isdir(dst))
        self.assertEqual(set(os.listdir(dst)), {'file.txt'})

    def test_recopy_full_dir_recursive(self):
        dst = os.path.join(self.stage, 'full_dir')
        mkdir(dst)
        open(os.path.join(dst, 'existing.txt'), 'w').close()

        subprocess.check_call(['doppel', '-r', 'full_dir', dst])
        self.assertTrue(os.path.isdir(dst))
        self.assertEqual(set(os.listdir(dst)), {'existing.txt', 'file.txt'})
