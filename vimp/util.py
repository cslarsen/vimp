"""
Vimp utility functions.

Copyright (C) 2014 Christian Stigen Larsen
Distributed under the LGPL v2.1; see LICENSE.txt
"""

import os
import shutil
import sys

from vimp.log import verb

def touch(path):
    """Creates an empty file."""  
    if not exists(path):
      verb("Touching %s" % path)
      with open(path, "w"):
          return

def joinpath(*args):
    """Joins paths."""
    return os.path.join(*args)

def mkdir(path):
    """Creates full directory path if it does not exist."""
    if not exists(path):
        verb("Creating directories %s" % path)
        os.makedirs(path)

def copyfile(src, dst):
    verb("Copy %s to %s" % (src, dst))
    shutil.copyfile(src, dst)

def pathname(path):
    """Return only path part of a full filename."""
    return os.path.split(path)[0]

def symlink(src, dst):
  """Creates a symlink at `dst` that points to `src`."""

  if exists(dst):
      verb("Symlink: Removing existing file %s" % dst)
      os.unlink(dst)

  if not exists(src):
      print("Error: Symlink source does not exist: %s" % src)
      sys.exit(1)
  if not exists(dst):
      # TODO: Shouldn't use pathname below, we only want to
      #       create directories UP TO the last part.
      mkdir(pathname(dst))

  verb("Symlinking %s -> %s" % (dst, src))
  os.symlink(src, dst)

def readlink(path):
    try:
        return os.readlink(path)
    except OSError:
        return None

def exists(path):
  if os.path.exists(path):
    verb("Exists %s? Yes" % path)
    return True
  else:
    verb("Exists %s? No" % path)
    return False

def unlinktree(*path):
    """Deletes entire directory."""
    path = joinpath(*path)
    if exists(path):
        verb("Removing tree %s" % path)
        shutil.rmtree(path)

def unlink(*path):
    """Delete file."""
    path = joinpath(*path)
    if exists(path):
        verb("Removing %s" % path)
        os.unlink(path)
    else:
      verb("Warning: Cannot remove non-existing path %s" % path)
