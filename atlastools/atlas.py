import os
from os.path import join as pjoin
import re
from functools import partial

from .archives import archive_version

VERSION_RE = re.compile(r'atlas([\d]+).(\d+).(\d+).tar')

atlas_archive_version = partial(archive_version, pattern=VERSION_RE)



