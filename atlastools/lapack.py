from __future__ import with_statement

import os
from os.path import join as pjoin
import re
from functools import partial

from distutils.sysconfig import parse_makefile

from .archives import archive_version
from .system import caller
from .makeparse import variable_sub


VERSION_RE = re.compile(r'[\w-]+(\d+).(\d+).(\d+)*')

archive_version = partial(archive_version, pattern=VERSION_RE)


def configure(build_dir, opts = None, incfile = 'make.inc.gfortran'):
    # identify, read, store make.inc template
    if not os.path.isabs(incfile):
        incfile = pjoin(build_dir, 'INSTALL', incfile)
    with open(incfile) as in_fobj:
        with open(pjoin(build_dir, 'make.inc'), 'wt') as out_fobj:
            context = variable_sub(in_fobj, out_fobj, opts)
    return context


def make(build_dir):
    pwd = os.getcwd()
    try:
        os.chdir(build_dir)
        caller('make lapacklib')
    finally:
        os.chdir(pwd)



