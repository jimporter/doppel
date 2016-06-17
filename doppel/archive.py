import os
import tarfile
from zipfile import ZipFile as _ZipFile


class ZipFile(object):
    def __init__(self, name, mode):
        self.__file = _ZipFile(name, mode)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.__file.close()

    def add(self, name, arcname=None, recursive=True):
        if arcname is None:
            arcname = name
        self.__file.write(name, arcname)

        if os.path.isdir(name) and recursive:
            for f in os.listdir(name):
                self.add(os.path.join(name, f), os.path.join(arcname, f),
                         recursive)


formats = ['gzip', 'bzip2', 'zip']
_fmts = {
    'gzip': (tarfile.open, 'w:gz'),
    'bzip2': (tarfile.open, 'w:bz2'),
    'zip': (ZipFile, 'w'),
}


def open(name, format):
    fn, mode = _fmts[format]
    return fn(name, mode)
