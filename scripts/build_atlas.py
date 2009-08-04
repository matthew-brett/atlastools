#!/usr/bin/env python
''' Script to build ATLAS locally

Atlas page is:

http://math-atlas.sourceforge.net/

'''

import os
from os.path import join as pjoin
from atlastools.system import caller
from atlastools.archives import extract_archive
from atlastools.atlas import atlas_archive_version


def build_in(out_dir, build_dir, flags=()):
    os.makedirs(build_dir)
    os.chdir(build_dir)
    caller((pjoin(out_dir, 'configure'),) + flags, shell=True)
    caller('make', shell=True)
    

def main():
    HOME = os.environ['HOME']
    ATLAS_ARCHIVE = pjoin(HOME, 'tmp', 'atlas3.9.11.tar.bz2')
    COMPILE_ROOT = pjoin(HOME, 'stable_trees', 'atlas2')
    OUT_SDIR = 'atlas-%s' % atlas_archive_version(ATLAS_ARCHIVE)
    OUT_DIR = pjoin(COMPILE_ROOT, OUT_SDIR)
    BUILD_DIR = pjoin(OUT_DIR, 'test_build')
    extract_archive(ATLAS_ARCHIVE, OUT_DIR)
    build_in(OUT_DIR, BUILD_DIR)


if __name__ == '__main__':
    main()
    
