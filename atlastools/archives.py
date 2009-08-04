import os
from os.path import join as pjoin
import shutil
import re
import tempfile
import tarfile


def archive_version(filename, pattern):
    ''' Extract archive version number from filename given ver '''
    if isinstance(pattern, basestring):
        pattern = re.compile(pattern)
    pth, fname = os.path.split(filename)
    match = pattern.match(fname)
    if match:
        return '.'.join(match.groups())
    raise ValueError('Could not get version from fname "%s"' %
                     fname)


def extract_archive(archive, out_dir, clobber=True):
    """ Extract `archive` into `out_dir`, overwriting if `clobber`

    More specifically, we expect this archive to unpack such that if we
    unpack in <tempdir>, there will be 1 and only one directory in
    <tempdir>.  If this subdirectory is <tempdir>/<some_dir>, then the
    result of this routine will be to move <tempdir>/<some_dir> so that
    it now has name <out_dir>.
    
    Parameters
    ----------
    archive : string
       archive filename
    out_dir : string
       absolute path of directory to move archive contents as
    clobber : bool
       If True, remove any previous contents of `out_dir`
    """
    tar = tarfile.open(archive)
    if os.path.exists(out_dir) and clobber:
        shutil.rmtree(out_dir)
    try:
        tmpdir = tempfile.mkdtemp()
        tar.extractall(tmpdir)
        tar.close()
        fnames = os.listdir(tmpdir)
        for dirpath, dirnames, filenames in os.walk(tmpdir):
            if len(dirnames) > 1:
                raise OSError('More than one directory in archive')
            break
        in_dir = pjoin(tmpdir, dirnames[0])
        shutil.copytree(in_dir, out_dir)
    finally:
        shutil.rmtree(tmpdir)


