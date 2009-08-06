import os
from os.path import join as pjoin
import shutil
import re
import tempfile
import tarfile


def archive_version(filename, pattern=None):
    ''' Extract archive version number from filename

    Parameters
    ----------
    filename : string
       filename that should contain a version number
    pattern : string or regexp object, optional
       Pattern to detect and return version number.  By default, the
       version number if of form 3.4.5, or 3.4 - that is at least a
       major and a minor version number separated by dots.  The pattern
       should return the version from::

          fname = os.path.split(filename)
          match = pattern.match(fname).group()

    Returns
    -------
    version : string
       string containing version number

    Raises
    ------
    ValueError, if there is not pattern match.

    Examples
    --------
    >>> archive_version('atlas-3.9.11.tar.gz')
    '3.9.11'
    >>> archive_version('lapack33.9')
    '33.9'
    >>> archive_version('lapack33')
    Traceback (most recent call last):
       ...
    ValueError: Could not get version from "lapack33"
    '''
    if pattern is None:
        pattern = r'(\d+\.)(\d+\.)?(\d+)'
    if isinstance(pattern, basestring):
        pattern = re.compile(pattern)
    pth, fname = os.path.split(filename)
    match = pattern.search(fname)
    if not match:
        raise ValueError('Could not get version from "%s"' %
                         fname)
    return match.group()


def extract_archive_to(archive, out_dir, clobber=True):
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


def prepare_for(archive, source_url):
    if not os.path.exists(archive):
        raise OSError('Cannot find %s; download from %s ?'
                      % (archive, source_url))
