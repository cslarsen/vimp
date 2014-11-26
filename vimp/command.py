"""
Implementation of vimp commands.

Copyright (C) 2014 Christian Stigen Larsen
Distributed under the LGPL v2.1; see LICENSE.txt
"""

import sys

from vimp import (__author__, __license__, __version__)
from vimp.install import (
    download_parallel,
    expandvars,
    get_full_name,
    get_script,
    get_short_name,
    getpath,
    install_script,
    isinstalled,
)
from vimp.util import (
    joinpath,
    readlink,
    unlink,
    unlinktree,
)
from vimp.log import verb
from vimp.scripts import SCRIPTS

def lookup_function(name):
    """
    Looks up function associated with command name.
    """
    if name not in COMMANDS and name not in COMMAND_ALIASES:
        print("Unknown command: %s" % name)
        sys.exit(1)
    else:
        if name in COMMAND_ALIASES:
            name = COMMAND_ALIASES[name]
        return COMMANDS[name]

def print_help(name=None):
    """
    Prints vimp help.
    """
    if name is None:
        print("%s %s by %s" % ("vimp", __version__, __author__))
        print("Usage: vimp [-v] command [ argument(s) ]")
        print("")
        print("vimp is a simple package manager for vim that downloads all")
        print("dependencies and enables them in vim for you.  It relies on")
        print("Pathogen, and will install it for you.")
        print("")
        print("Known commands:")
        print(", ".join(sorted(COMMANDS.keys())))
        print("")
        print("Examples:")
        print("vimp ls # show installed packages")
        print("vimp ls -a # list all available packages")
        print("vimp install fuzzyfinder # install l9 and fuzzyfinder")
        print("vimp disable fuzzyfinder # disable but do not delete")
        print("vimp help install # show help for install")
        print("vimp get -v ctrlp # install ctrlp and show all actions")
        print("")
        print("It works by creating symlinks from ~/.vim/bundle/ to")
        print("~/.vimp/install and adds a command in ~/.vimrc that")
        print("reads extra settings from ~/.vimp/vimrc")
        print("")
        print("This is currently in early alpha-stages, so a lot of")
        print("things don't work.  But installing and uninstalling does.")
        return

    function = lookup_function(name)
    if function is None:
        print("Unknown command: '%s'" % name)
        sys.exit(1)
    else:
        # TODO: Print function signature

        if name in COMMAND_ALIASES:
            print("%s is an alias for %s\n" % (name, COMMAND_ALIASES[name]))
            name = COMMAND_ALIASES[name]
        print("Help for vimp command %s:" % name)

        print(function.__doc__)
        sys.exit(1)


def version(*a):
    """
    Prints program version and exits.
    """
    print("vimp %s" % __version__)
    print("Made by %s" % __author__)
    print(__license__)
    sys.exit(0)

def print_version():
    print("vimp %s" % __version__)
    print("Written by %s" % __author__)
    print(__license__)

def garbage_collect():
    # TODO: Remove files in installed/ that do not have symlinks from vim
    # TODO: Delete cache dir
    # TODO: If script A requires B and C and you uninstall A, then we should
    # also remove B and C if no other installed scripts require them.
    # (Only exception is if you actually WANT to install B).
    # Solution: A refcount somewhere _could_ work, but is prone to getting
    # out of sync.  Perhaps a flag may be enough (i.e., refcount from 0 to
    # 1).
    raise NotImplementedError()

def install(*names):
  """
  Installs vim script with given name.
  """
  # For many items, download everything in parallel
  urls = set()

  def add(n):
    s = get_script(n)
    if "download" not in s:
      return
    url, arch = s["download"]
    arch = joinpath(getpath("download", n), expandvars(n, arch))
    urls.update([(n, url, arch)])

  # Add pathogen dependency
  if not isinstalled("pathogen") and "pathogen" not in names:
    names = ("pathogen",) + names

  for n in names:
    s = get_script(n)
    if "deps" in s:
      for dep in s["deps"]:
        add(dep)
    add(n)

  download_parallel(list(urls))
  install_rest(*names)

def install_rest(name=None, *rest):
    """
    Installs vim script with given name.
    """
    if name is None:
        return

    if not isinstalled(name):
        script = get_script(name)
        deps = script["deps"] if "deps" in script else []

        # We don't *have* to install dependencies first. So we'll install
        # the plugin in question here. This should also work in the case
        # someone creates circular dependencies.
        install_script(name, script)

        # Now install dependencies recursively
        if len(deps) > 0:
          print("%s depends on %s" % (name, " ".join(deps)))
          install_rest(*deps)
    else:
        print("%s is already installed" % name)

    # Continue installing any remaining plugins
    install_rest(*rest)


def disable(name, *rest, **kw):
    """
    Disables a vim script without deleting it from disk.
    """
    if not isinstalled(name):
        print("Script %s is not installed" % name)
        sys.exit(0)

    if "log" in kw and kw["log"]==False:
      pass
    else:
      print("Disabling %s" % name)

    # Remove symlinks
    s = get_script(name)
    for (_,dst) in s["symlink"]:
        dst = expandvars(name, dst)
        if readlink(dst) != None:
            verb("Removing symlink %s" % dst)
            unlink(dst)

def remove(name, *rest):
    """
    Disables a vim script and removes it from disk.
    """
    if isinstalled(name):
        disable(name, log=False)

    full = get_full_name(name)
    print("Removing %s" % full)
    unlinktree(getpath("install"), full)
    unlinktree(getpath("download"), full)

    if len(rest) > 0:
      remove(*rest)


def list_all(FLAG_L):
  """Lists all known scripts."""
  width = max(map(len, SCRIPTS.keys()))
  print("All available plugins")
  for name in sorted(SCRIPTS.keys()):
    s = get_script(name)
    if FLAG_L:
      print("%-*s %s" % (width, get_full_name(name),
                         expandvars(name, s["about"])))
    else:
      print(name)

def list_details(name):
    s = get_script(name)
    print("%s by %s" % (s["name"], s["author"]))
    if "about" in s:
        print(expandvars(name, s["about"]))
    print("%s" % s["download"][0])
    if "deps" in s and len(s["deps"]) > 0:
        print("Dependencies: %s" % " ".join(s["deps"]))

    if "print" in s:
        for l in s["print"]:
            print(expandvars(name, l))

    print("Installed: %s" % ("Yes" if isinstalled(name) else "No"))

def list_installed(*args):
    """Print list of installed or available scripts.

    Use -l to include version and description.

    Use -a to list all available plugins. If -a is not specified, will list
    installed plugins only.
    """
    # Parse flags
    FLAG_A = False
    FLAG_L = False
    for arg in args:
        if arg.startswith("-"):
          for char in arg[1:]:
            if char == "a": FLAG_A = True
            elif char == "l": FLAG_L = True
            else:
              print("Unknown list flag: %s" % arg)
              sys.exit(1)
        else:
          list_details(arg)
          return

    # List all scripts
    if FLAG_A:
      list_all(FLAG_L)
      return

    # List installed scripts
    installed = [n for n in SCRIPTS if isinstalled(n)]
    if len(installed) == 0:
      print("You have not installed any scripts.")
      print("You can view all available scripts with `vimp ls -a`")
    else:
      print("Installed plugins")
      width = max(map(len, installed))
      for n in sorted(installed):
        s = get_script(n)
        if FLAG_L:
            print("%-*s %s" % (width, get_full_name(n), s["about"]))
        else:
            print("%s" % get_short_name(n))

def update():
    """
    Update list of vim scripts from the net.
    """
    raise NotImplementedError()

def upgrade(name=None):
    """
    Upgrades vim scripts.
    """
    raise NotImplementedError()


def search(name=None, *rest):
    """
    Search for vim scripts and suggested matches.
    """
    def phonetically_similar(candidate, fuzz):
      # This is an old heuristic that actually performs quite well: Remove
      # all vowels and compare.  Means that "powrlaine" will match
      # "powerline". Furthermore, remove double letters, and translate
      # some consonants such as C to K, etc.

      def no_vowels(s):
        """Removes all vowels in string."""
        return "".join(c for c in s if c not in "aeiouy")

      def no_repeats(s):
        """Removes repeated characters in string."""
        if len(s) <= 1:
            return s
        else:
            return s[0] + "".join(s[n] if s[n]!=s[n-1] else ""
                                  for n in xrange(1,len(s)))

      def simplify(s):
        """Change q->k, w->v, z->s etc. to simplify comparison."""
        tr = {"q":"k", "w":"v", "z":"s", "c":"k"}
        return "".join(tr[c] if c in tr else c for c in s)

      def phonetic(s):
        return no_repeats(no_vowels(simplify(s)))

      a = phonetic(candidate)
      b = phonetic(fuzz)

      return (a==b) or (a in b) or (b in a)

    def keyword_match(name, s):
      """Check if name matches keywords."""
      if "keywords" in s:
        for keyword in s["keywords"]:
          if (keyword in name) or (name in keyword):
            return True
      return False

    if name is None:
      return
    else:
      name = name.lower()

    for n in sorted(SCRIPTS):
      match = (name in n) | (n in name)
      match |= phonetically_similar(name, n)
      match |= keyword_match(name, get_script(n))

      if match:
        s = get_script(n)
        if "about" in s:
          print("%s - %s" % (n, expandvars(n, s["about"])))
        else:
          print("%s" % n)

def switch(previous, new):
    """
    Just a cleverly named shorthand for disabling the first package and
    installing the second.
    """
    disable(previous)
    install(new)

# Associate command name with function.
COMMANDS = {
    "disable": disable,
    "help": print_help,
    "install": install,
    "list": list_installed,
    "remove": remove,
    "search": search,
    "switch": switch,
    "version": version,
}

COMMAND_ALIASES = {
    "add": "install",
    "enable": "install",
    "find": "search",
    "get": "install",
    "info": "list",
    "ls": "list",
    "rm": "remove",
    "swap": "switch",
    "uninstall": "disable",
}
