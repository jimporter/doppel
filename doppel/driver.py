import argparse
import os

from . import copy, makedirs
from .version import version

description = """
doppel copies files or directories to a destination directory, similar to
install(1). By default, if only one source is specified, it is copied *onto*
the destination; if multiple sources are specified, they are copied *into* the
destination.
"""


def mode(s):
    return int(s, 8)


def main():
    parser = argparse.ArgumentParser(prog='doppel', description=description)
    parser.add_argument('source', nargs='*', help='source files/directories')
    parser.add_argument('dest', help='destination')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-o', '--onto', action='store_true', dest='onto',
                       default=None, help='copy source onto dest')
    group.add_argument('-i', '--into', action='store_false', dest='onto',
                       help='copy sources into dest')

    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + version)
    parser.add_argument('-p', '--parents', action='store_true',
                        help='make parent directories as needed')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='recurse into subdirectories')
    parser.add_argument('-m', '--mode', metavar='MODE', type=mode,
                        help='set file mode (as octal)')
    parser.add_argument('-C', '--directory', metavar='DIR', default='.',
                        help='change to directory DIR before copying')
    parser.add_argument('-N', '--full-name', action='store_true',
                        help='use the full name of the source when copying')

    args = parser.parse_args()
    if args.onto is None:
        args.onto = len(args.source) == 1

    os.chdir(args.directory)
    try:
        if args.onto:
            if len(args.source) != 1:
                parser.error('exactly one source required')
            if args.parents:
                makedirs(os.path.dirname(args.dest), exist_ok=True)
            copy(args.source[0], args.dest, args.recursive, args.mode)
        else:
            if args.parents:
                makedirs(args.dest, exist_ok=True)
            for src in args.source:
                if args.full_name:
                    dirname = os.path.dirname(src)
                    if args.parents and dirname:
                        makedirs(os.path.join(args.dest, dirname),
                                 exist_ok=True)
                    tail = src
                else:
                    tail = os.path.basename(src)

                copy(src, os.path.join(args.dest, tail),
                     args.recursive, args.mode)
    except Exception as e:
        parser.error(e)
