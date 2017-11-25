import subprocess

from .. import *


class TestErrors(unittest.TestCase):
    def test_onto_and_format(self):
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.check_output(['doppel', '--onto', '--format', 'zip',
                                     'dest'], stderr=subprocess.STDOUT)

    def test_dest_prefix_without_format(self):
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.check_output(['doppel', '--dest-prefix', 'prefix',
                                     'dest'], stderr=subprocess.STDOUT)

    def test_onto_multiple_sources(self):
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.check_output(['doppel', '--onto', 'src1', 'src2',
                                     'dest'], stderr=subprocess.STDOUT)
