import os
import shutil

from .. import *
from doppel import makedirs, mkdir, require_dirs


class TestRequireDirs(unittest.TestCase):
    def setUp(self):
        os.chdir(this_dir)
        stage = os.path.join(test_stage_dir, 'require_dirs')
        if os.path.exists(stage):
            shutil.rmtree(os.path.join(stage))
        makedirs(stage)
        os.chdir(stage)

    def test_empty(self):
        require_dirs('')
        assertDirectory('.', {})

    def test_create_existing_directory(self):
        mkdir('directory')
        require_dirs('directory')
        assertDirectory('.', {
            'directory',
        })

    def test_create_existing_file(self):
        open('file.txt', 'w').close()
        self.assertRaises(OSError, require_dirs, 'file.txt')

    def test_create_nonexistent(self):
        require_dirs('directory')
        assertDirectory('.', {
            'directory',
        })

    def test_no_create_existing_directory(self):
        mkdir('directory')
        require_dirs('directory', create=False)
        assertDirectory('.', {
            'directory',
        })

    def test_no_create_existing_file(self):
        open('file.txt', 'w').close()
        self.assertRaises(IOError, require_dirs, 'file.txt', create=False)

    def test_no_create_nonexistent(self):
        self.assertRaises(IOError, require_dirs, 'nonexist', create=False)
