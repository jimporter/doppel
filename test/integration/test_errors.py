import subprocess

from .. import *


def check_output(command):
    return subprocess.check_output(command, stderr=subprocess.STDOUT,
                                   universal_newlines=True)


class TestErrors(unittest.TestCase):
    def test_onto_and_format(self):
        with self.assertRaises(subprocess.CalledProcessError):
            check_output(['doppel', '--onto', '--format', 'zip', 'dest'])

    def test_dest_prefix_without_format(self):
        with self.assertRaises(subprocess.CalledProcessError):
            check_output(['doppel', '--dest-prefix', 'prefix', 'dest'])

    def test_onto_multiple_sources(self):
        with self.assertRaises(subprocess.CalledProcessError):
            check_output(['doppel', '--onto', 'src1', 'src2', 'dest'])

    def test_dest_nonexistent(self):
        os.chdir(test_data_dir)
        with self.assertRaises(subprocess.CalledProcessError) as e:
            check_output(['doppel', '--into', 'src', 'nonexist'])
        self.assertEqual(e.exception.output,
                         "doppel: directory 'nonexist' does not exist\n")

    def test_dest_is_not_directory(self):
        os.chdir(test_data_dir)
        with self.assertRaises(subprocess.CalledProcessError) as e:
            check_output(['doppel', '--into', 'src', 'file.txt'])
        self.assertEqual(e.exception.output,
                         "doppel: 'file.txt' is not a directory\n")

    def test_make_parents_dest_is_not_directory(self):
        os.chdir(test_data_dir)
        with self.assertRaises(subprocess.CalledProcessError) as e:
            check_output(['doppel', '--into', '-p', 'src', 'file.txt'])
        self.assertEqual(e.exception.output,
                         "doppel: 'file.txt' is not a directory\n")
