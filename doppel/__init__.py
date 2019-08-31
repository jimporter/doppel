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


def parent_dir(path):
    return os.path.normpath(os.path.join(path, os.pardir))


def existing_parent(path):
    while not os.path.exists(path):
        path = parent_dir(path)
    return path


def remove(path, nonexist_ok=False):
    try:
        os.remove(path)
    except OSError as e:
        if not nonexist_ok or e.errno != errno.ENOENT:
            raise


def copy(src, dst, recursive=False, symlink='relative', mode=None):
    if symlink != 'never' and os.path.islink(src):
        link = os.readlink(src)
        if symlink == 'always' or not os.path.isabs(link):
            remove(dst, nonexist_ok=True)
            os.symlink(link, dst)
            return

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
