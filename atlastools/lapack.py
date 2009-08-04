from __future__ import with_statement

import os
from os.path import join as pjoin
import re
from functools import partial

from distutils.sysconfig import parse_makefile

from .archives import archive_version
from .system import caller

VERSION_RE = re.compile(r'[\w-]+(\d+).(\d+).(\d+)*')

archive_version = partial(archive_version, pattern=VERSION_RE)


def build(build_dir, opts = None, incfile = 'make.inc.gfortran'):
    pwd = os.getcwd()
    # identify, read, store make.inc template
    if not os.path.isabs(incfile):
        incfile = pjoin(build_dir, 'INSTALL', incfile)
    make_dict = parse_makefile(incfile)
    with open(incfile) as fobj:
        lines = fobj.readlines()
    # use template and fill in new values
    if opts:
        lines.append('# Extra options for build')
        for item in opts.items():
            lines.append('%s = %s\n' % item)
    # write new make.inc
    with open(pjoin(build_dir, 'make.inc'), 'wt') as fobj:
        fobj.writelines(lines)
    try:
        os.chdir(build_dir)
        caller('make lapacklib')
    finally:
        os.chdir(pwd)
    return pjoin(build_dir, make_dict['LAPACKLIB'])
    

