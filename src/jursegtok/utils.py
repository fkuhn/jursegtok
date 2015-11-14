#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import errno

_ROOT = os.path.abspath(os.path.dirname(__file__))

def create_dir(path):
    """
    Creates a directory. Warns, if the directory can't be accessed. Passes,
    if the directory already exists.
    modified from http://stackoverflow.com/a/600612
    Parameters
    ----------
    path : str
        path to the directory to be created
    """
    import os
    import sys
    import errno

    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST:
            if os.path.isdir(path):
                pass
            else:  # if something exists at the path, but it's not a dir
                raise
        elif exc.errno == errno.EACCES:
            sys.stderr.write("Cannot create [%s]! Check Permissions" % path)
            raise
        else:
            raise

def get_data(dataitem):
def find_files(directory, pattern='*'):
    """
    find files recursively, e.g. all *.txt files
    in a given directory (or its subdirectories)

    adapted from: http://stackoverflow.com/a/2186673
    """
    import os
    import fnmatch

    abspath = os.path.abspath(os.path.expanduser(directory))
    for root, dirs, files in os.walk(abspath):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename
    """
    given a _ROOT, returns the absolute path of a given data item
    """
    return os.path.join(_ROOT, 'data', dataitem)
