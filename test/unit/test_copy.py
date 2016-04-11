import os
import unittest
import shutil

from doppel import copy

this_dir = os.path.abspath(os.path.dirname(__file__))
test_data_dir = os.path.join(this_dir, '..', 'data')
test_stage_dir = os.path.join(this_dir, '..', 'stage')


class TestCopy(unittest.TestCase):
    def setUp(self):
        self.stage = os.path.join(test_stage_dir, 'copy')
        if os.path.exists(self.stage):
            shutil.rmtree(os.path.join(self.stage))
        os.makedirs(self.stage)
        os.chdir(test_data_dir)

    def test_copy_file(self):
        dst = os.path.join(self.stage, 'file.txt')
        copy('file.txt', dst)
        self.assertTrue(os.path.isfile(dst))

    def test_recopy_file(self):
        dst = os.path.join(self.stage, 'file.txt')
        open(dst, 'w').close()
        copy('file.txt', dst)
        self.assertTrue(os.path.isfile(dst))

    def test_copy_empty_dir(self):
        dst = os.path.join(self.stage, 'empty_dir')
        copy('empty_dir', dst)
        self.assertTrue(os.path.isdir(dst))
        self.assertEqual(os.listdir(dst), [])

    def test_recopy_empty_dir(self):
        dst = os.path.join(self.stage, 'full_dir')
        os.mkdir(dst)
        open(os.path.join(dst, 'file.txt'), 'w').close()

        copy('empty_dir', dst)
        self.assertTrue(os.path.isdir(dst))
        self.assertEqual(set(os.listdir(dst)), {'file.txt'})

    def test_copy_full_dir(self):
        dst = os.path.join(self.stage, 'full_dir')
        copy('full_dir', dst)
        self.assertTrue(os.path.isdir(dst))
        self.assertEqual(set(os.listdir(dst)), {'file.txt'})

    def test_recopy_full_dir(self):
        dst = os.path.join(self.stage, 'full_dir')
        os.mkdir(dst)
        open(os.path.join(dst, 'existing.txt'), 'w').close()

        copy('full_dir', dst)
        self.assertTrue(os.path.isdir(dst))
        self.assertEqual(set(os.listdir(dst)), {'existing.txt', 'file.txt'})
