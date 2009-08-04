#!/usr/bin/env python
''' Script to build LAPACK locally

ftp://ftp.netlib.org/lapack/

'''
from __future__ import with_statement

import os
from os.path import join as pjoin
from atlastools.archives import extract_archive
from atlastools.lapack import archive_version, build


HOME = os.environ['HOME']
LAPACK_ARCHIVE = pjoin(HOME, 'tmp', 'lapack-lite-3.1.1.tgz')
COMPILE_ROOT = pjoin(HOME, 'stable_trees', 'atlas2')
OUT_SDIR = 'lapack-%s' % archive_version(LAPACK_ARCHIVE)
OUT_DIR = pjoin(COMPILE_ROOT, OUT_SDIR)


def main():
    extract_archive(LAPACK_ARCHIVE, OUT_DIR)
    build(OUT_DIR)


if __name__ == '__main__':
    main()
    
