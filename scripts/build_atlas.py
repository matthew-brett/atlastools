#!/usr/bin/env python
''' Script to build ATLAS locally

Atlas page is:

http://math-atlas.sourceforge.net/

'''

import os
from os.path import join as pjoin
from atlastools import caller, extract_archive, atlas, get_cpuinfo


HOME = os.environ['HOME']
ATLAS_ARCHIVE = pjoin(HOME, 'tmp', 'atlas3.9.11.tar.bz2')
COMPILE_ROOT = pjoin(HOME, 'stable_trees', 'atlas')
OUT_SDIR = 'atlas-%s' % atlas.archive_version(ATLAS_ARCHIVE)
OUT_DIR = pjoin(COMPILE_ROOT, OUT_SDIR)
BUILD_DIR = pjoin(OUT_DIR, 'test_build')
LAPACK_FILE = pjoin(COMPILE_ROOT, 'lapack-3.2.1/lapack_X64_SSE3.a')
FLAGS = '-b 64 -Fa alg "-fPIC -msse3" -D c "-DPentiumCPS=%f" --with-netlib-lapack=%s' \
    % (get_cpuinfo()[0]['cpu MHz'], LAPACK_FILE)


def main():
    extract_archive(ATLAS_ARCHIVE, OUT_DIR)
    atlas.configure_in(OUT_DIR, BUILD_DIR, FLAGS)
    print atlas.make_script(BUILD_DIR)

if __name__ == '__main__':
    main()
    
