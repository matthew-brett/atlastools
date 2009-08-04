#!/usr/bin/env python
''' Script to build ATLAS locally

Atlas page is:

http://math-atlas.sourceforge.net/

'''

import os
from os.path import join as pjoin
from atlastools.system import caller
from atlastools.archives import extract_archive
from atlastools.atlas import archive_version, build_in


HOME = os.environ['HOME']
ATLAS_ARCHIVE = pjoin(HOME, 'tmp', 'atlas3.9.11.tar.bz2')
COMPILE_ROOT = pjoin(HOME, 'stable_trees', 'atlas2')
OUT_SDIR = 'atlas-%s' % archive_version(ATLAS_ARCHIVE)
OUT_DIR = pjoin(COMPILE_ROOT, OUT_SDIR)
BUILD_DIR = pjoin(OUT_DIR, 'test_build')
FLAGS = ()


def main():
    extract_archive(ATLAS_ARCHIVE, OUT_DIR)
    build_in(OUT_DIR, BUILD_DIR, FLAGS)


if __name__ == '__main__':
    main()
    
