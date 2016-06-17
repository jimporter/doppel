import argparse
import os
import tarfile

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
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + version)

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-o', '--onto', action='store_true', dest='onto',
                       default=None, help='copy source onto dest')
    group.add_argument('-i', '--into', action='store_false', dest='onto',
                       help='copy sources into dest')

    parser.add_argument('-p', '--parents', action='store_true',
                        help='make parent directories as needed')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='recurse into subdirectories')
    parser.add_argument('-f', '--format', metavar='FMT',
                        choices=['tgz', 'tbz2'],
                        help='format of output file (one of: %(choices)s)')
    parser.add_argument('-m', '--mode', metavar='MODE', type=mode,
                        help='set file mode (as octal)')
    parser.add_argument('-C', '--directory', metavar='DIR', default='.',
                        help='change to directory DIR before copying')
    parser.add_argument('-N', '--full-name', action='store_true',
                        help='use the full name of the source when copying')
    parser.add_argument('--dest-prefix', metavar='DIR',
                        help='a prefix to add to destination files')

    parser.add_argument('source', nargs='*', help='source files/directories')
    parser.add_argument('dest', help='destination')

    args = parser.parse_args()
    if args.onto is True and args.format:
        parser.error('--format cannot be used with --onto')
    if args.onto is None:
        args.onto = len(args.source) == 1 and args.format is None

    try:
        if args.onto:
            if len(args.source) != 1:
                parser.error('exactly one source required')
            if args.parents:
                makedirs(os.path.dirname(args.dest), exist_ok=True)
            copy(os.path.join(args.directory, args.source[0]), args.dest,
                 args.recursive, args.mode)
        elif args.format:
            with tarfile.open(args.dest, 'w:' + args.format[1:]) as f:
                for src in args.source:
                    dst = src if args.full_name else os.path.basename(src)
                    if args.dest_prefix:
                        dst = os.path.join(args.dest_prefix, dst)
                    f.add(os.path.join(args.directory, src), dst,
                          recursive=args.recursive)
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

                copy(os.path.join(args.directory, src),
                     os.path.join(args.dest, tail),
                     args.recursive, args.mode)
    except Exception as e:
        parser.error(e)
