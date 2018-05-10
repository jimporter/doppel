import argparse
import elevate
import os

from . import archive, copy, existing_parent, makedirs, parent_dir
from .version import version

description = """
doppel copies files or directories to a destination (a file, directory, or
archive). Think of it as the offspring of install(1) and tar(1). By default, if
only one source is specified, it is copied *onto* the destination; if multiple
sources are specified, they are copied *into* the destination.
"""


def mode(s):
    return int(s, 8)


def report_error(parser, error, code=1):
    parser.exit(code, '{prog}: {error}\n'.format(
        prog=parser.prog, error=str(error)
    ))


def maybe_makedirs(path, create, *args, **kwargs):
    if create:
        makedirs(path, *args, **kwargs)


def main():
    parser = argparse.ArgumentParser(prog='doppel', description=description)
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + version)
    parser.add_argument('--sudo', metavar='WHEN',
                        choices=['always', 'never', 'auto'], default='auto',
                        help=('elevate to root (one of: %(choices)s; ' +
                              'default: %(default)s)'))
    parser.add_argument('-S', action='store_const', const='always',
                        dest='sudo', help=('elevate to root (equivalent to ' +
                                           '`--sudo=always`)'))
    parser.add_argument('source', metavar='SOURCE', nargs='*',
                        help='source files/directories')
    parser.add_argument('dest', metavar='DEST', help='destination')

    input_p = parser.add_argument_group('input arguments')

    onto_p = input_p.add_mutually_exclusive_group()
    onto_p.add_argument('-o', '--onto', action='store_true', dest='onto',
                        default=None, help='copy SOURCE onto DEST')
    onto_p.add_argument('-i', '--into', action='store_false', dest='onto',
                        help='copy SOURCEs into DEST')

    input_p.add_argument('-r', '--recursive', action='store_true',
                         help='recurse into subdirectories')
    input_p.add_argument('-C', '--directory', metavar='DIR', default='.',
                         help='change to directory DIR before copying')

    output_p = parser.add_argument_group('output arguments')

    output_p.add_argument('-p', '--parents', action='store_true',
                          help='make parent directories as needed')
    output_p.add_argument('-m', '--mode', metavar='MODE', type=mode,
                          help='set file mode (as octal)')
    output_p.add_argument('-N', '--full-name', action='store_true',
                          help='use the full name of the source when copying')

    archive_p = parser.add_argument_group('archive-specific arguments')
    archive_p.add_argument('-f', '--format', metavar='FMT',
                           choices=archive.formats,
                           help='format of output file (one of: %(choices)s)')
    archive_p.add_argument('-P', '--dest-prefix', metavar='DIR',
                           help='a prefix to add to destination files')

    args = parser.parse_args()
    if args.onto is True and args.format:
        parser.error('--format cannot be used with --onto')
    if args.dest_prefix and not args.format:
        parser.error('--dest-prefix can only be used with --format')
    if args.onto is None:
        args.onto = len(args.source) == 1 and args.format is None

    if args.onto and len(args.source) != 1:
        parser.error('exactly one source required')

    destdir = (parent_dir(args.dest) if args.onto or args.format
               else args.dest)
    if args.parents:
        parent = existing_parent(destdir)
        if not os.path.isdir(parent):
            report_error(parser, "'{}' is not a directory".format(parent))
    else:
        if not os.path.exists(destdir):
            report_error(parser, ("directory '{}' does not exist"
                                  .format(destdir)))
        elif not os.path.isdir(destdir):
            report_error(parser, "'{}' is not a directory".format(destdir))

    # No coverage here since re-running this process with root breaks coverage
    # reporting...
    if args.sudo == 'always' or (args.sudo == 'auto' and not os.access(
        existing_parent(args.dest), os.W_OK
    )):  # pragma: no cover
        elevate.elevate(graphical=False)

    try:
        if args.onto:
            maybe_makedirs(destdir, exist_ok=True, create=args.parents)
            copy(os.path.join(args.directory, args.source[0]), args.dest,
                 args.recursive, args.mode)
        elif args.format:
            maybe_makedirs(destdir, exist_ok=True, create=args.parents)
            with archive.open(args.dest, 'w', args.format) as f:
                for src in args.source:
                    dst = src if args.full_name else os.path.basename(src)
                    if args.dest_prefix:
                        dst = os.path.join(args.dest_prefix, dst)
                    f.add(os.path.join(args.directory, src), dst,
                          args.recursive, args.mode)
        else:
            maybe_makedirs(destdir, exist_ok=True, create=args.parents)
            for src in args.source:
                if args.full_name:
                    dirname = os.path.dirname(src)
                    if dirname:
                        makedirs(os.path.join(args.dest, dirname),
                                 exist_ok=True)
                    tail = src
                else:
                    tail = os.path.basename(src)

                copy(os.path.join(args.directory, src),
                     os.path.join(args.dest, tail),
                     args.recursive, args.mode)
    except Exception as e:  # pragma: no cover
        report_error(parser, e)
