#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import errno


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
            else: # if something exists at the path, but it's not a dir
                raise
        elif exc.errno == errno.EACCES:
            sys.stderr.write("Cannot create [%s]! Check Permissions" % path)
            raise
        else:
            raise
