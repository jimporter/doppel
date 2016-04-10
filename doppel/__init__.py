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


def copy(src, dst, mode=None):
    if os.path.isdir(src):
        mkdir(dst, exist_ok=True)
        for name in os.listdir(src):
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            copy(srcname, dstname)
    else:
        shutil.copyfile(src, dst)
        if mode:
            os.chmod(dst, mode)
        else:
            shutil.copymode(src, dst)
