import os
from os.path import join as pjoin
import re
from functools import partial

from .archives import archive_version
from .system import caller

VERSION_RE = re.compile(r'atlas([\d]+).(\d+).(\d+).tar')

archive_version = partial(archive_version, pattern=VERSION_RE)


def build_in(out_dir, build_dir, flags=()):
    os.makedirs(build_dir)
    os.chdir(build_dir)
    caller((pjoin(out_dir, 'configure'),) + flags)
    caller('make')
    




