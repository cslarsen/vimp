"""
Configuration of vimp.

Copyright (C) 2014 Christian Stigen Larsen
Distributed under the LGPL v2.1; see LICENSE.txt
"""

import os
import pickle

from vimp.install import getpath
from vimp.log import verb
from vimp.scripts import (SCRIPTS, __version__ as SCRIPTS_VER)
from vimp.util import (touch, joinpath, mkdir)

VIMRC_INCLUDE = '    exec ":source" . $HOME . "/.vimp/vimrc"'

VIMRC_COMPLETE = """
\" =============== Vimp Initialization ===============
\" This section enables vimp as a package manager, and
\" was automatically added by vimp. Sorry for that!
\"
\" If you delete ~/.vimp/ then you can also remove
\" this section, if you want to.

  if filereadable($HOME . "/.vimp/vimrc")
""" + VIMRC_INCLUDE + """
  endif

"""

VIMPRC_HEADER = """" This file is maintained by vimp
"""


def vimrc_links_to_vimp():
    """Check if user's vimrc links to vimp."""
    with open(getpath("vimrc"), "rt") as f:
        for l in f.readlines():
          if l.startswith(VIMRC_INCLUDE):
                return True
    return False

def write_repo(version_scripts):
    """Writes repository version/script to vimp dir."""
    version, scripts = version_scripts
    scripts = joinpath(getpath("list"), "scripts")
    with open(scripts, "wb") as f:
        f.write(pickle.dumps((version, scripts), protocol=2))

def read_repo():
    """Return (version, scripts) from vimp dir."""
    scripts = joinpath(getpath("list"), "scripts")
    if os.path.exists(scripts):
        with open(scripts, "rb") as f:
            return pickle.loads(f.read())
    return (None, None)

def link_vimrc_to_vimp():
    """Creates a link from user's vimrc to vimp."""
    verb("Adding vimp hook in ~/.vimrc")
    with open(getpath("vimrc"), "at") as f:
        f.write(VIMRC_COMPLETE)

def configure():
    """
    Performs configuration of vimp.
    If no ~/.vimp/ exists, creates it.
    """
    global SCRIPTS

    touch(getpath("vimrc"))

    vimpdir = getpath("vimp")
    listdir = getpath("list")
    instdir = getpath("install")
    dldir = getpath("download")
    vimplugin = joinpath(getpath("vim"), "plugin")
    autoload = joinpath(getpath("vim"), "autoload")

    # Create required directories
    for path in [vimpdir, listdir, instdir, dldir, vimplugin, autoload]:
        mkdir(path)

    # Create .vimp/vimrc
    vimrc = joinpath(vimpdir, "vimrc")
    if not os.path.exists(vimrc):
        with open(vimrc, "wt") as f:
            f.write(VIMPRC_HEADER)

    # Include our vimrc in user's vimrc
    if not vimrc_links_to_vimp():
        link_vimrc_to_vimp()

    # Update scripts repository if needed
    as_tuple = lambda s: tuple(map(int, s.split(".")))
    (rver, rscr) = read_repo()
    if (rver is None) or (as_tuple(SCRIPTS_VER) > as_tuple(rver)):
        write_repo((SCRIPTS_VER, SCRIPTS))

