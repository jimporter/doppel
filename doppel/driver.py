import argparse
import os

from . import copy, makedirs
from .version import version


def main():
    parser = argparse.ArgumentParser(prog='doppel')
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
    parser.add_argument('-m', '--mode', metavar='MODE',
                        help='set file mode (as in chmod)')

    args = parser.parse_args()
    if args.onto is None:
        args.onto = len(args.source) == 1

    if args.onto:
        if len(args.source) != 1:
            raise ValueError('FIXME')
        if args.parents:
            makedirs(os.path.dirname(args.dest), exist_ok=True)
        copy(args.source[0], args.dest)
    else:
        if args.parents:
            makedirs(args.dest, exist_ok=True)
        for src in args.source:
            copy(src, os.path.join(args.dest, os.path.basename(src)))
