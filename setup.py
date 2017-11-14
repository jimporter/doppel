import re
from setuptools import setup, find_packages
from doppel.version import version

custom_cmds = {}

try:
    from flake8.main.setuptools_command import Flake8

    class LintCommand(Flake8):
        def distribution_files(self):
            return ['setup.py', 'doppel', 'test']

    custom_cmds['lint'] = LintCommand
except ImportError:
    pass

with open('README.md', 'r') as f:
    # Read from the file and strip out the badges.
    long_desc = re.sub(r'(^# doppel)\n\n(.+\n)*', r'\1', f.read())

try:
    import pypandoc
    long_desc = pypandoc.convert(long_desc, 'rst', format='md')
except ImportError:
    pass

setup(
    name='doppel',
    version=version,

    description='A friendly file copier/installer',
    long_description=long_desc,
    keywords='file copier and installer',
    url='https://github.com/jimporter/doppel',

    author='Jim Porter',
    author_email='porterj@alum.rit.edu',
    license='BSD',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',

        'Intended Audience :: Developers',

        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    packages=find_packages(exclude=['test', 'test.*']),

    extras_require={
        'deploy': ['pypandoc'],
        'lint': ['flake8'],
    },

    entry_points={
        'console_scripts': [
            'doppel=doppel.driver:main',
        ]
    },

    test_suite='test',
    cmdclass=custom_cmds,
)
