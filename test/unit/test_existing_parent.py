import os
import unittest
import shutil

from doppel import existing_parent

this_dir = os.path.abspath(os.path.dirname(__file__))
test_stage_dir = os.path.join(this_dir, '..', 'stage')


class TestExistingParent(unittest.TestCase):
    def setUp(self):
        os.chdir(this_dir)
        stage = os.path.join(test_stage_dir, 'existing_parent')
        if os.path.exists(stage):
            shutil.rmtree(os.path.join(stage))
        os.makedirs(stage)
        os.chdir(stage)

    def test_existent(self):
        os.mkdir('subdir')
        self.assertEqual(existing_parent('subdir'), 'subdir')
        self.assertEqual(existing_parent('subdir/nonexist'), 'subdir')

    def test_nonexistent(self):
        self.assertEqual(existing_parent('nonexist'), '.')
        self.assertEqual(existing_parent('./nonexist'), '.')
        self.assertEqual(existing_parent('../nonexist'), '..')
