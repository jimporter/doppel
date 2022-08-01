import os
import subprocess
import re
from setuptools import setup, find_packages, Command

from doppel.version import version

root_dir = os.path.abspath(os.path.dirname(__file__))


class Coverage(Command):
    description = 'run tests with code coverage'
    user_options = [
        ('test-suite=', 's',
         "test suite to run (e.g. 'some_module.test_suite')"),
    ]

    def initialize_options(self):
        self.test_suite = None

    def finalize_options(self):
        pass

    def run(self):
        env = dict(os.environ)
        pythonpath = os.path.join(root_dir, 'test', 'scripts')
        if env.get('PYTHONPATH'):
            pythonpath += os.pathsep + env['PYTHONPATH']
        env.update({
            'PYTHONPATH': pythonpath,
            'COVERAGE_FILE': os.path.join(root_dir, '.coverage'),
            'COVERAGE_PROCESS_START': os.path.join(root_dir, '.coveragerc'),
        })

        subprocess.run(['coverage', 'erase'], check=True)
        subprocess.run(
            ['coverage', 'run', 'setup.py', 'test'] +
            (['-q'] if self.verbose == 0 else []) +
            (['-s', self.test_suite] if self.test_suite else []),
            env=env, check=True
        )
        subprocess.run(['coverage', 'combine'], check=True,
                       stdout=subprocess.DEVNULL)


custom_cmds = {
    'coverage': Coverage,
}

with open(os.path.join(root_dir, 'README.md'), 'r') as f:
    # Read from the file and strip out the badges.
    long_desc = re.sub(r'(^# doppel)\n\n(.+\n)*', r'\1', f.read())

setup(
    name='doppel',
    version=version,

    description='A friendly file copier/installer',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    keywords='file copier and installer',
    url='https://github.com/jimporter/doppel',

    author='Jim Porter',
    author_email='itsjimporter@gmail.com',
    license='BSD',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],

    packages=find_packages(exclude=['test', 'test.*']),

    install_requires=['elevate >= 0.1.2'],
    extras_require={
        'test': ['coverage', 'flake8 >= 3.0', 'flake8-quotes'],
    },

    entry_points={
        'console_scripts': [
            'doppel=doppel.driver:main',
        ]
    },

    test_suite='test',
    cmdclass=custom_cmds,
)
