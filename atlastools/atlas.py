import os
from os.path import join as pjoin
import re
from functools import partial
from StringIO import StringIO

from .archives import archive_version
from .system import caller

VERSION_RE = re.compile(r'atlas([\d]+).(\d+).(\d+).tar')

archive_version = partial(archive_version, pattern=VERSION_RE)


def configure_in(src_dir, build_dir, flags=''):
    os.makedirs(build_dir)
    pwd = os.getcwd()
    try:
        os.chdir(build_dir)
        caller(pjoin(src_dir, 'configure') + ' ' + flags)
    finally:
        os.chdir(pwd)


def make_script(build_dir):
    sio = StringIO()
    sio.write('cd %s\n' % build_dir)
    sio.write('make build\n')
    sio.write('make check\n')
    sio.write('make time\n')
    sio.write('cd lib\n')
    sio.write('make shared\n')
    sio.write('make ptshared\n')
    return sio.getvalue()


