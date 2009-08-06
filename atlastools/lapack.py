from __future__ import with_statement

import os
from os.path import join as pjoin

from .makeparse import variable_sub
from .archives import extract_archive_to
from .system import make_targets

def configure(build_dir, opts = None, incfile = 'make.inc.gfortran'):
    # identify, read, store make.inc template
    if not os.path.isabs(incfile):
        incfile = pjoin(build_dir, 'INSTALL', incfile)
    with open(incfile) as in_fobj:
        with open(pjoin(build_dir, 'make.inc'), 'wt') as out_fobj:
            context = variable_sub(in_fobj, out_fobj, opts)
    return context


def build(archive, src_dir, opts):
    extract_archive_to(archive, src_dir)
    configure(src_dir, opts)
    make_targets(src_dir, ('lapacklib',))


