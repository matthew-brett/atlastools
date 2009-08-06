#!/usr/bin/env python
''' Script to build LAPACK and ATLAS locally

ftp://ftp.netlib.org/lapack/
http://sourceforge.net/projects/math-atlas/files/

'''
from __future__ import with_statement

import os
from os.path import join as pjoin
from urllib import urlretrieve

from atlastools import lapack, atlas, archive_version
from atlastools import get_cpuinfo, prepare_for


HOME = os.environ['HOME']

# Change these to suit your setup
SOURCE_ROOT = pjoin(HOME, 'stable_trees', 'atlas')
ARCHIVE_DIR = pjoin(SOURCE_ROOT, 'archives')
LAPACK_ARCHIVE = pjoin(ARCHIVE_DIR, 'lapack-3.2.1.tgz')
LAPACK_URL = 'ftp://ftp.netlib.org/lapack'
ATLAS_ARCHIVE = pjoin(ARCHIVE_DIR, 'atlas3.9.11.tar.bz2')
ATLAS_URL = 'http://sourceforge.net/projects/math-atlas/files'
BUILD_TYPE = 64 # one of 64 or 32
COMPILE_FLAGS = '-m%s -fPIC -msse3' % BUILD_TYPE
PLATFORM = 'X64_SSE3'
TO_LINK_DIR = pjoin(HOME, 'blas_lapack')

# Change these if you like, but they should take care of themselves
LAPACK_DIR = pjoin(SOURCE_ROOT, 'lapack-%s' % archive_version(LAPACK_ARCHIVE))
ATLAS_DIR = pjoin(SOURCE_ROOT, 'atlas-%s' % archive_version(ATLAS_ARCHIVE))
LAPACK_OPTS = {'PLAT': '_' + PLATFORM,
        'OPTS': '-O2 ' + COMPILE_FLAGS,
        'NOOPT': '-O0 ' + COMPILE_FLAGS}
LAPACK_LIB = pjoin(LAPACK_DIR, 'lapack_%s.a' % PLATFORM)
ATLAS_BUILD_DIR = pjoin(ATLAS_DIR, 'builds', PLATFORM)
CPU_MHZ = get_cpuinfo()[0]['cpu MHz']
ATLAS_FLAGS = ('-b %(BUILD_TYPE)s ' + 
    '-Fa alg "%(COMPILE_FLAGS)s" ' + 
    '-D c "-DPentiumCPS=%(CPU_MHZ)f" ' + 
    '--with-netlib-lapack=%(LAPACK_LIB)s') % locals()


def main():
    prepare_for(LAPACK_ARCHIVE, LAPACK_URL)
    prepare_for(ATLAS_ARCHIVE, ATLAS_URL)
    lapack.build(LAPACK_ARCHIVE, LAPACK_DIR, LAPACK_OPTS)
    atlas.build_in(ATLAS_ARCHIVE, ATLAS_DIR, ATLAS_BUILD_DIR, ATLAS_FLAGS)
    atlas.copy_required(ATLAS_BUILD_DIR, TO_LINK_DIR)


if __name__ == '__main__':
    main()
    
