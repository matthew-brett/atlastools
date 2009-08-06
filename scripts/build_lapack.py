#!/usr/bin/env python
''' Script to build LAPACK locally

ftp://ftp.netlib.org/lapack/

'''
from __future__ import with_statement

import os
from os.path import join as pjoin
from atlastools import extract_archive, lapack


HOME = os.environ['HOME']
LAPACK_ARCHIVE = pjoin(HOME, 'tmp', 'lapack-3.2.1.tgz')
COMPILE_ROOT = pjoin(HOME, 'stable_trees', 'atlas')
OUT_SDIR = 'lapack-%s' % lapack.archive_version(LAPACK_ARCHIVE)
OUT_DIR = pjoin(COMPILE_ROOT, OUT_SDIR)
OPTS = {'PLAT': '_X64_SSE3',
        'OPTS': '-O2 -m64 -fPIC -msse3',
        'NOOPT': '-O0 -m64 -fPIC -msse3'}


def main():
    extract_archive(LAPACK_ARCHIVE, OUT_DIR)
    context = lapack.configure(OUT_DIR, OPTS)
    lapack.make(OUT_DIR)
    print context


if __name__ == '__main__':
    main()
    
