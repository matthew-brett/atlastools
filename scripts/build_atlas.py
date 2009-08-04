#!/usr/bin/env python
''' Script to build ATLAS locally

Atlas page is:

http://math-atlas.sourceforge.net/

'''

import os
from os.path import join as pjoin
import sys
from functools import partial
import re
import tempfile
import tarfile
import shutil
from subprocess import check_call, Popen, PIPE

HOME = os.environ['HOME']
atlas_archive = pjoin(HOME, 'tmp', 'atlas3.9.11.tar.bz2')
compile_root = pjoin(HOME, 'stable_trees', 'atlas')
BUILD_SDIR = 'test_build'


caller = partial(check_call, shell=True)


def atlas_archive_version(filename):
    version_re = re.compile(r'atlas([\d]+).(\d+).(\d+).tar')
    pth, fname = os.path.split(filename)
    match = version_re.match(fname)
    if match:
        return '.'.join(match.groups())
    raise ValueError('Could not get version from fname "%s"' %
                     fname)


def extract_archive(atlas_archive, compile_root, clobber=True):
    tar = tarfile.open(atlas_archive)
    out_sdir = 'atlas-%s' % atlas_archive_version(atlas_archive)
    out_dir = pjoin(compile_root, out_sdir)
    if os.path.exists(out_dir) and clobber:
        shutil.rmtree(out_dir)
    try:
        tmpdir = tempfile.mkdtemp()
        tar.extractall(tmpdir)
        tar.close()
        fnames = os.listdir(tmpdir)
        for dirpath, dirnames, filenames in os.walk(tmpdir):
            if len(dirnames) > 1:
                raise OSError('More than one directory in Atlas archive')
            break
        in_dir = pjoin(tmpdir, dirnames[0])
        shutil.copytree(in_dir, out_dir)
    finally:
        shutil.rmtree(tmpdir)
    return out_dir


def build_in(out_dir, build_dir, flags=()):
    if not os.path.isabs(build_dir):
        build_dir = pjoin(out_dir, build_dir)
    os.makedirs(build_dir)
    os.chdir(build_dir)
    caller((pjoin(out_dir, 'configure'),) + flags, shell=True)
    caller('make', shell=True)
    

def main():
    out_dir = extract_archive(atlas_archive, compile_root)
    build_in(out_dir, BUILD_SDIR)


if __name__ == '__main__':
    main()
    
