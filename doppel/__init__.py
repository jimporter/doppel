import errno
import os
import shutil


def mkdir(path, mode=0o777, exist_ok=False):
    try:
        os.mkdir(path, mode)
    except OSError as e:
        if not exist_ok or e.errno != errno.EEXIST or not os.path.isdir(path):
            raise


def makedirs(path, mode=0o777, exist_ok=False):
    try:
        os.makedirs(path, mode)
    except OSError as e:
        if not exist_ok or e.errno != errno.EEXIST or not os.path.isdir(path):
            raise


def require_dirs(path, mode=0o777, create=True):
    if not path:
        return
    if create:
        makedirs(path, mode, exist_ok=True)
    elif not os.path.exists(path):
        raise IOError("directory '{}' does not exist".format(path))
    elif not os.path.isdir(path):
        raise IOError("'{}' is not a directory".format(path))


def copy(src, dst, recursive=False, mode=None):
    if os.path.isdir(src):
        mkdir(dst, exist_ok=True)
        if recursive:
            for name in os.listdir(src):
                copy(os.path.join(src, name), os.path.join(dst, name))
    else:
        shutil.copyfile(src, dst)
        if mode is not None:
            os.chmod(dst, mode)
        else:
            shutil.copymode(src, dst)
