# doppel

[![PyPi version][pypi-image]][pypi-link]
[![Travis build status][travis-image]][travis-link]
[![Appveyor build status][appveyor-image]][appveyor-link]
[![Coverage status][codecov-image]][codecov-link]

**doppel** copies files or directories to a destination (a file, directory, or
archive). Think of it as the offspring of
[*install(1)*](http://linux.die.net/man/1/install) and
[*tar(1)*](http://linux.die.net/man/1/tar).

## Usage

```
doppel [OPTION]... SOURCE... DEST
```

To copy files or directories, just list the sources as arguments followed by
the destination: `doppel src1 src2 dst`. By default, if only one source is
specified, it is copied *onto* the destination; if multiple sources are
specified, they are copied *into* the destination. This default can be
explicitly specified with `-o/--onto` or `-i/--into`, respectively.

If the destination requires administrator access to write to, doppel will try to
detect this an automatically provide a `sudo` (or equivalent) prompt before
copying.

*Note:* Unlike *install(1)*, doppel copies relative symlinks as symlinks by
default. To adjust this behavior, you can use the `--symlink` option, described
below.

## Options

### -C, --directory=DIR

Change to directory `DIR` before resolving paths of source files.

### -f, --format=FMT

Set the format of the output archive; one of: `tar`, `gzip`, `bzip2`, or `zip`.
If this option is specified, `--into` is implied. If not set, source files will
be copied normally, and no archive will be created.

### -i, --into

Copy sources into directory `DEST`.

### -m, --mode=MODE

Set the file permissions to `MODE` (an octal) when copying. Note: this has no
effect when `--format=zip`.

### -N, --full-name

When copying, use the full name of each source file as specified on the command
line instead of just the tail. This behavior is similar to
[*tar(1)*](http://linux.die.net/man/1/tar).

### -o, --onto

Copy a single source onto file or directory `DEST`.

### -p, --parents

Automatically create parent directories for `DEST` as needed.

### -P, --dest-prefix=DIR

A prefix to add to the paths of destination files. This only applies when using
`--format`.

### -r, --recursive

Recursively copy source directories to the destination.

### -S, --sudo=WHEN

Before copying, elevate with `sudo` (or your platform's equivalent). `WHEN` is
one of `always`, `auto` (the default), or `never`. If `auto`, doppel will
attempt to determine automatically if `sudo` would be needed before performing
the copy.

### --symlink=WHEN

Copy symlinks as links. `WHEN` is one of `always`, `relative` (the default), or
`never`. If `relative`, only symlinks with relative targets will be copied as
symlinks; those with absolute targets will be copied as regular files.

### @file

Read options from `file` and use them when executing.

### --help

Display a help message and exit.

### --version

Output version information and exit.

## License

This project is licensed under the [BSD 3-clause license](LICENSE).

[pypi-image]: https://img.shields.io/pypi/v/doppel.svg
[pypi-link]: https://pypi.python.org/pypi/doppel
[travis-image]: https://travis-ci.org/jimporter/doppel.svg?branch=master
[travis-link]: https://travis-ci.org/jimporter/doppel
[appveyor-image]: https://ci.appveyor.com/api/projects/status/uuyc9b1g73urehap/branch/master?svg=true
[appveyor-link]: https://ci.appveyor.com/project/jimporter/doppel/branch/master
[codecov-image]: https://codecov.io/gh/jimporter/doppel/branch/master/graph/badge.svg
[codecov-link]: https://codecov.io/gh/jimporter/doppel
