import os
from collections import OrderedDict
from tarfile import TarFile as _TarFile
from zipfile import ZipFile as _ZipFile

_open = open


class ZipFile(_ZipFile):
    def add(self, name, arcname=None, recursive=True, mode=None):
        if arcname is None:
            arcname = name
        self.write(name, arcname)

        if os.path.isdir(name) and recursive:
            for f in os.listdir(name):
                self.add(os.path.join(name, f), os.path.join(arcname, f),
                         recursive)


class TarFile(_TarFile):
    def add(self, name, arcname=None, recursive=True, mode=None):
        if arcname is None:
            arcname = name

        info = self.gettarinfo(name, arcname)
        if info.isreg():
            if mode is not None:
                info.mode = mode
            with _open(name, 'rb') as f:
                self.addfile(info, f)
        elif info.isdir():
            self.addfile(info)
            if recursive:
                for f in os.listdir(name):
                    self.add(os.path.join(name, f), os.path.join(arcname, f),
                             recursive, mode)
        else:
            self.addfile(info)


_fmts = OrderedDict(
    tar=TarFile.taropen,
    gzip=TarFile.gzopen,
    bzip2=TarFile.bz2open,
    zip=ZipFile,
)
formats = list(_fmts.keys())


def open(name, mode, format):
    return _fmts[format](name, mode)
