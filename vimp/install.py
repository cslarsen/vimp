"""
Installation of vim packages.

Copyright (C) 2014 Christian Stigen Larsen
Distributed under the LGPL v2.1; see LICENSE.txt
"""

from zipfile import ZipFile
import contextlib
import os
import shutil
import sys
import tarfile
import threading

try:
    import urllib2
except ImportError:
    import urllib

from vimp.log import (verb)
from vimp.scripts import (SCRIPTS, ALIASES)
from vimp.util import (
    copyfile,
    exists,
    joinpath,
    mkdir,
    pathname,
    readlink,
    symlink,
    unlinktree,
)


def get_full_name(name):
    return ALIASES[name] if name in ALIASES else name

def get_short_name(fullname):
    for k in ALIASES.keys():
      if ALIASES[k] == fullname:
        return k
    return fullname

def has_vimprc(text):
    vimprc = getpath("vimprc")
    with open(vimprc, "rt") as f:
        for l in f.readlines():
            if l.startswith(text):
                return True
    return False

def remove_vimprc(name, text):
    verb("Warning: Unimplemented remove_vimprc")
    pass

def add_vimprc(name, lines):
    """Adds a line to .vimp/vimrc."""
    tab = "  "
    indent = 0

    if len(lines) == 0:
        return

    # Check if text is already there
    header = "\" ==== %s ====" % name
    if has_vimprc(header):
        verb("There is already an entry in .vimp/vimrc for %s" % name)
        return

    verb("Adding entry for %s to .vimp/vimrc" % name)
    with open(getpath("vimprc"), "at") as f:
        f.write("\n" + header + "\n")

        # Check if symlinks exists before executing commands
        s = get_script(name)
        tab = "  "
        for (_, dst) in s["symlink"]:
            dst = expandvars(name, dst)
            f.write(tab*indent + "if filereadable(\"%s\")\n" % dst)
            indent += 1

        for line in lines:
            f.write(tab*indent + "%s\n" % expandvars(name, line))

        for (_, dst) in s["symlink"]:
            indent -= 1
            f.write(tab*indent + "endif\n")

def helptags(name, path):
    s =  "if !filereadable(\"%s/tags\")\n" % path
    s += "  call pathogen#helptags()\n"
    s += "endif\n"
    return s

def getpath(label, name=""):
    """Returns full path to various parts of vimp and vim."""
    full = get_full_name(name)
    vimp = os.path.expanduser(joinpath("~", ".vimp"))
    vimrc = os.path.expanduser(joinpath("~", ".vimrc"))
    vim = os.path.expanduser(joinpath("~", ".vim"))

    def unknown_label():
        print("Error: Unknown path label: %s" % label)
        sys.exit(1)

    # Poor man's switch-statement (I don't like long if-elif blocks, sorry!)
    return {
        "vim":      lambda: vim,
        "list":     lambda: joinpath(vimp, "list"),
        "vimrc":    lambda: vimrc,
        "vimp":     lambda: vimp,
        "vimprc":   lambda: joinpath(vimp, "vimrc"),
        "install":  lambda: joinpath(vimp, "installed", full),
        "bundle":   lambda: joinpath(vim, "bundle", get_short_name(name)),
        "download": lambda: joinpath(vimp, "download", full),
        "colors":   lambda: joinpath(vim, "colors"),
     }.get(label, unknown_label)()

def download(url, filename, skip_existing=True):
    """Stores download in .vimp/downloads/ and returns filename."""
    if exists(filename) and skip_existing:
        return
    else:
        mkdir(pathname(filename))

    verb("Downloading %s -> %s" % (url, filename))
    resp = urllib2.urlopen(url)
    with open(filename, "wb") as f:
        f.write(resp.read())
    resp.close()

def download_parallel(urls_files):
  """Download list of (url, file) tuples in parallel."""
  threads = []
  names = []
  for (name, url, filename) in urls_files:
    if exists(filename):
      continue
    names.append(name)
    thread = threading.Thread(target=download, args=(url, filename, True))
    threads.append(thread)

  if len(threads) > 0:
    if len(names) > 1:
      print("Downloading %d packages in parallel: %s" % (
        len(names), " ".join(names)))
    else:
      print("Downloading %s" % " ".join(names))

    map(lambda s: s.start(), threads)
    map(lambda s: s.join(), threads)

@contextlib.contextmanager
def zipfile(path):
    z = ZipFile(path)
    yield z
    z.close()

@contextlib.contextmanager
def zipfile_member(zipobj, member):
    f = zipobj.open(member)
    yield f
    f.close()

def unzip_member(zipobj, member, output):
    with zipfile_member(zipobj, member) as src:
        mkdir(pathname(output))
        with file(output, "wb") as dst:
            shutil.copyfileobj(src, dst)

def unzip_members(archive, pairs):
    """From archive, unzip (member, destination) from pairs."""
    with zipfile(archive) as z:
        members = z.namelist()

        for pattern, output in pairs:
            # Poor man's glob
            if pattern.endswith("*"):
                for member in members:
                    base = os.path.basename(member)
                    dest = joinpath(output, base)
                    if member.startswith(pattern[:-1]):
                        verb("Unzipping %s -> %s" % (member, dest))
                        unzip_member(z, member, dest)
            else:
                verb("Unzipping %s -> %s" % (pattern, output))
                unzip_member(z, pattern, output)

@contextlib.contextmanager
def open_tarfile(path):
    t = tarfile.open(path, "r")
    yield t
    t.close()

def untar_member(tar, member, output):
    mkdir(pathname(output))

    if member.isdir():
        return

    name = member.get_info("utf-8", None)["name"]
    verb("Untar %s to %s" % (name, output))

    member.name = os.path.basename(output)
    tar.extract(member, pathname(output))

def untargz_members(archive, pairs):
    def get(tarinfo, field):
        return tarinfo.get_info("utf-8", None)[field]

    with open_tarfile(archive) as t:
        members = t.getmembers()

        for pattern, output in pairs:
            # Poor man's glob
            if pattern.endswith("*"):
                for info in members:
                    member = get(info, "name")
                    base = os.path.basename(member)
                    dest = joinpath(output, base)
                    if member.startswith(pattern[:-1]):
                        untar_member(t, info, dest)
            else:
                for info in members:
                    member = get(info, "name")
                    if member == pattern:
                        base = os.path.basename(member)
                        dest = joinpath(output, base)
                        untar_member(t, info, output)
                        break

def extract(archive, pairs):
  """Extract member from archive and save to output filename."""
  verb("Extracting %s" % archive)

  base, ext = os.path.splitext(archive)
  if ext == ".zip":
      unzip_members(archive, pairs)
  elif archive.endswith(".tar.gz"):
      untargz_members(archive, pairs)
  else:
      print("Error: Unknown archive type: %s" % archive)

def expandvars(name, s):
  variables = {
      "bundle": getpath("bundle", name),
      "download": getpath("download", name),
      "colors": getpath("colors"),
      "install": getpath("install", name),
      "name": name,
      "fullname": get_full_name(name),
      "shortname": get_short_name(name),
      "vim": getpath("vim"),
      "CR": "\r\n",
  }
  return s.format(**variables)

def install_script(name, script):
  print("Installing %s" % name)

  def expand(s):
    return expandvars(name, s)

  def expand_all(pairs):
      out = []
      for a, b in pairs:
          out.append((expand(a), expand(b)))
      return out

  archive = None

  if "download" in script:
    url, archive = script["download"]
    archive = joinpath(getpath("download", name), expand(archive))
    download(url, archive)

  if "extract" in script:
    extract(archive, expand_all(script["extract"]))

  if "embed" in script:
    for (filename, text) in script["embed"]:
      filename = expand(filename)
      text = expand(text)
      mkdir(pathname(filename))
      with open(filename, "wt") as f:
          f.write(text)

  if "copy" in script:
    for (src, dst) in script["copy"]:
      mkdir(pathname(expand(dst)))
      copyfile(expand(src), expand(dst))

  if "symlink" in script:
    for (src, dst) in script["symlink"]:
      symlink(expand(src), expand(dst))

  # Add helptags
  if not name.startswith("pathogen"):
    vimrc = helptags(name, expand("{bundle}/doc")).split("\n")
    vimrc = vimrc[0:-1]
  else:
    vimrc = []
  if "vimrc" in script:
      vimrc += script["vimrc"]
  add_vimprc(name, vimrc)

  # Remove download
  unlinktree(getpath("download", get_full_name(name)))

  if "print" in script:
      for line in script["print"]:
          print(expand(line))

def get_script(name):
    # Lookup aliases first
    if name in ALIASES.keys():
      name = ALIASES[name]

    if name in SCRIPTS.keys():
        script = SCRIPTS[name]
        script["name"] = name
        return script
    else:
        print("Unknown script: %s" % name)
        sys.exit(1)

def isinstalled(name):
    """Check if script is installed."""
    def yes(): verb("Is installed %s? Yes" % name); return True
    def no(): verb("Is installed %s? No" % name); return False

    # Special handling for pathogen
    if name == "pathogen":
        path = joinpath(getpath("vim"), "autoload", "pathogen.vim")
        if exists(path):
          return yes()
        else:
          return no()

    # First of all, the install directory must exist
    if not exists(getpath("install", name)):
      return no()

    # Now we check that all symlinks have been installed (we check that
    # these are _actual_ symlinks pointing to .vimp/installed).
    s = get_script(name)
    for (src, dst) in s["symlink"]:
      src = expandvars(name, src)
      dst = expandvars(name, dst)

      if not exists(src):
        return no()

      if not exists(dst):
        return no()

      if readlink(dst) != src:
        return no()

    return yes()
