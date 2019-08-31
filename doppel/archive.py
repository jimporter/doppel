import os
import tarfile
import zipfile
from collections import OrderedDict

_open = open


class ZipFile(zipfile.ZipFile):
    def add(self, name, arcname=None, recursive=True, symlink='relative',
            mode=None):
        if arcname is None:
            arcname = name
        self.write(name, arcname)

        if os.path.isdir(name) and recursive:
            for f in os.listdir(name):
                self.add(os.path.join(name, f), os.path.join(arcname, f),
                         recursive)


class TarFile(tarfile.TarFile):
    def add(self, name, arcname=None, recursive=True, symlink='relative',
            mode=None):
        if arcname is None:
            arcname = name

        info = self.gettarinfo(name, arcname)
        if info.issym():
            if ( symlink == 'never' or
                 (symlink == 'relative' and os.path.isabs(info.linkname)) ):
                info.type = tarfile.REGTYPE

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
