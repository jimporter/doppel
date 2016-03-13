from setuptools import setup, find_packages
from doppel.version import version

with open('README.md', 'r') as f:
    long_desc = f.read()

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
    url='https://github.com/jimporter/doppel'

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
    },

    entry_points={
        'console_scripts': [
            'doppel=doppel.driver:main',
        ]
    },
)
