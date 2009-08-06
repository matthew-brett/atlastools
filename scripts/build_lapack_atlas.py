#!/usr/bin/env python
''' Script to build LAPACK and ATLAS locally

ftp://ftp.netlib.org/lapack/

'''
from __future__ import with_statement

import os
from os.path import join as pjoin
from urllib import urlretrieve

from atlastools import lapack, atlas, archive_version
from atlastools import get_cpuinfo


HOME = os.environ['HOME']

# Change these to suit your setup
SOURCE_ROOT = pjoin(HOME, 'stable_trees', 'atlas')
ARCHIVE_DIR = pjoin(SOURCE_ROOT, 'archives')
LAPACK_FILE = 'lapack-3.2.1.tgz'
ATLAS_FILE = 'atlas3.9.11.tar.bz2'
BUILD_TYPE = 64 # one of 64 or 32
COMPILE_FLAGS = '-m%s -fPIC -msse3' % BUILD_TYPE
PLATFORM = 'X64_SSE3'

# Change these if you like, but they should take care of themselves
LAPACK_ARCHIVE = pjoin(ARCHIVE_DIR, LAPACK_FILE)
LAPACK_DIR = pjoin(SOURCE_ROOT, 'lapack-%s' % archive_version(LAPACK_ARCHIVE))
LAPACK_URL = pjoin('http://www.netlib.org/lapack', LAPACK_FILE)
ATLAS_ARCHIVE = pjoin(ARCHIVE_DIR, ATLAS_FILE)
_atlas_version = archive_version(ATLAS_ARCHIVE)
ATLAS_DIR = pjoin(SOURCE_ROOT, 'atlas-%s' % _atlas_version)
ATLAS_URL = pjoin('http://downloads.sourceforge.net/project/math-atlas/Developer\\ (unstable)/%s' % _atlas_version, ATLAS_FILE)
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
    if not os.path.exists(LAPACK_ARCHIVE):
        raise OSError(
            'Cannot find archive %s; download from %s?' %
            (LAPACK_ARCHIVE, LAPACK_URL))
    lapack.build(LAPACK_ARCHIVE, LAPACK_DIR, LAPACK_OPTS)
    if not os.path.exists(ATLAS_ARCHIVE):
        raise OSError(
            'Cannot find archive %s; download from %s?' %
            (ATLAS_ARCHIVE, ATLAS_URL))
    atlas.build_in(ATLAS_ARCHIVE, ATLAS_DIR, ATLAS_BUILD_DIR, ATLAS_FLAGS)
    

if __name__ == '__main__':
    main()
    
