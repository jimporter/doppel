import os
import unittest
import shutil

from doppel import mkdir, makedirs

this_dir = os.path.abspath(os.path.dirname(__file__))
test_stage_dir = os.path.join(this_dir, '..', 'stage')


class TestMkdir(unittest.TestCase):
    def setUp(self):
        stage = os.path.join(test_stage_dir, 'mkdir')
        if os.path.exists(stage):
            shutil.rmtree(os.path.join(stage))
        os.makedirs(stage)
        os.chdir(stage)

    def test_dir(self):
        mkdir('foo')
        self.assertTrue(os.path.isdir('foo'))

    def test_existing_dir(self):
        mkdir('foo')
        self.assertRaises(OSError, mkdir, 'foo')

    def test_exist_ok(self):
        mkdir('foo')
        mkdir('foo', exist_ok=True)
        self.assertTrue(os.path.isdir('foo'))


class TestMakedirs(unittest.TestCase):
    def setUp(self):
        stage = os.path.join(test_stage_dir, 'makedirs')
        if os.path.exists(stage):
            shutil.rmtree(os.path.join(stage))
        os.makedirs(stage)
        os.chdir(stage)

    def test_dir(self):
        makedirs('foo')
        self.assertTrue(os.path.isdir('foo'))

    def test_existing_dir(self):
        makedirs('foo')
        self.assertRaises(OSError, makedirs, 'foo')

    def test_exist_ok(self):
        makedirs('foo')
        makedirs('foo', exist_ok=True)
        self.assertTrue(os.path.isdir('foo'))

    def test_nested_dir(self):
        makedirs('foo/bar')
        self.assertTrue(os.path.isdir('foo/bar'))

    def test_nested_existing_dir(self):
        makedirs('foo/bar')
        self.assertRaises(OSError, makedirs, 'foo/bar')

    def test_nested_exist_ok(self):
        makedirs('foo/bar')
        makedirs('foo/bar', exist_ok=True)
        self.assertTrue(os.path.isdir('foo/bar'))
