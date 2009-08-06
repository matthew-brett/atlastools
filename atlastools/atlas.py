import os
from os.path import join as pjoin

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


