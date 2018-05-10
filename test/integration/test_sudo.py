import os
import platform
import shutil
import subprocess

from .. import *
from doppel import makedirs

platform_name = platform.system()


class TestSudo(unittest.TestCase):
    def setUp(self):
        self.stage = os.path.join(test_stage_dir, 'sudo')
        if os.path.exists(self.stage):
            shutil.rmtree(os.path.join(self.stage))
        makedirs(self.stage)
        os.chdir(test_data_dir)

    @unittest.skipIf(platform_name == 'Windows', 'only text on posix')
    def test_sudo(self):
        env = dict(os.environ)
        env['PATH'] = test_data_dir + os.pathsep + env.get('PATH', '')

        dst = os.path.join(self.stage, 'file.txt')
        output = subprocess.check_output(['doppel', '-S', 'file.txt', dst],
                                         universal_newlines=True, env=env)
        self.assertEqual(output, 'this is a fake sudo\n')
