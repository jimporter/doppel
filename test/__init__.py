import os
import unittest

from itertools import chain

this_dir = os.path.abspath(os.path.dirname(__file__))
test_data_dir = os.path.join(this_dir, 'data')
test_stage_dir = os.path.join(this_dir, 'stage')


def assertDirectory(path, contents):
    path = os.path.normpath(path)
    actual = set(os.path.normpath(os.path.join(path, base, f))
                 for base, dirs, files in os.walk(path)
                 for f in chain(files, dirs))
    expected = set(os.path.normpath(os.path.join(path, i)) for i in contents)
    if actual != expected:
        missing = [os.path.relpath(i, path) for i in (expected - actual)]
        extra = [os.path.relpath(i, path) for i in (actual - expected)]
        raise unittest.TestCase.failureException(
            'missing: {}, extra: {}'.format(missing, extra)
        )
