from __future__ import with_statement
import os
from os.path import join as pjoin
import sys
from glob import glob
import shutil

from .archives import extract_archive_to
from .system import caller, make_targets


def configure_in(src_dir, build_dir, flags=''):
    os.makedirs(build_dir)
    pwd = os.getcwd()
    print pjoin(src_dir, 'configure') + ' ' + flags
    try:
        os.chdir(build_dir)
        caller(pjoin(src_dir, 'configure') + ' ' + flags)
    finally:
        os.chdir(pwd)


def build_in(archive, src_dir, build_dir, flags):
    extract_archive_to(archive, src_dir)
    configure_in(src_dir, build_dir, flags)
    make_targets(build_dir, ('build',))
    print '''Consider:
cd %s
make check
make time
''' % build_dir


def copy_required(build_dir, output_dir):
    ''' Copy Numpy-required files into output directory '''
    if sys.platform == 'win32':
        libext = 'lib'
    else:
        libext = 'a'
    include_dir = pjoin(output_dir, 'include')
    lib_dir = pjoin(output_dir, 'lib')
    for dirpath in (include_dir, lib_dir):
        try:
            os.makedirs(dirpath)
        except OSError:
            pass
    built_lib_search = pjoin(build_dir, 'lib', '*.%s' % libext)
    libs = glob(built_lib_search)
    if not libs:
        raise RuntimeError('Cannot find libs with search "%s"' %
                           built_lib_search)
    for fpath in libs:
        shutil.copy2(fpath, lib_dir)
    with open(pjoin(output_dir, 'site.cfg'), 'wt') as fobj:
        fobj.write(
'''[DEFAULT]
include_dirs = %s
library_dirs = %s

[blas_opt]
libraries = f77blas, cblas, atlas

[lapack_opt]
libraries = lapack, f77blas, cblas, atlas
''' % (include_dir, lib_dir))
    
