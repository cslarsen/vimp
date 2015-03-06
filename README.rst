vimp
====

Vimp is a simple plugin manager for vim that downloads and installs
plugins and dependencies, updating helptags along the way. In short, by
typing

::

    $ vimp get undotree@ctrl-u

vimp will download undotree, install it in vim and map it to CTRL-U
(``<C-U>``). If you decide you don't want undotree anymore (or just want
to disable the mapping on ctrl-u), type

::

    $ vimp disable undotree@ctrl-u

Warning
-------

While vimp currently works fine, it should be considered pre-release
alpha grade quality. Meaning that I actively experiment with it, and may
break stuff without notice at the current phase.

Also, you may want to backup your entire ``~/.vim`` directory and
``~/.vimrc`` file before experimenting. Using vimp should be quite safe
at this time, but just in case you really don't want to mess with your
setup, please backup.

Finally, vimp does not recognize your existing plugins. It *does* work
fine side-by-side with existing plugins, but I haven't done much testing
in this situation (a future version of vimp may be able to annex
existing plugins, we'll see).

More examples
-------------

Anyway, you can also specify several plugins to install. On a fresh or
existing vim installation, you can install a lot of stuff by typing:

::

    $ vimp get molokai powerline ctrlp signify nerdtree@ctrl-d \
      undotree@ctrl-u snipmate

This will download all the plugins above and their dependencies, and
will do so *in parallel*. It will also map NerdTree to and UndoTree to .
As this is a fresh vim install, it will install Pathogen also (note: it
does *not* enable vim plugins for you, but this is something it probably
should in a future version).

In the above example, it will also change the current color scheme to
Molokai. To switch from Molokai to the grb256 color scheme, just type:

::

    $ vimp switch molokai grb256

To disable a package, e.g. NERDTree, type

::

    $ vimp disable nerdtree@ctrl-d

and to actually remove it from disk, use the ``remove`` command. To list
installed packages, type ``vimp ls`` and to list all available type
``vimp ls -a``.

Vimp is in early stages of development, so expect bugs and lots of
changes. I made it for myself, so I don't care about any of the other
managers.

By the way, it does depend on Pathogen and will install it by default.
This is strictly not necessary, but I like Pathogen, so that's that for
the moment.

If you like vimp, let me know. The way to put forward suggestions is to
provide patches. If something is broken, let me know.

How it works
------------

It downloads vim packages to ``~/.vimp/cache/``, extracts files to a
staging area ``~/.vimp/installed`` and creates symlinks pointing to it
from ``~/.vim/bundle``.

To enable stuff like Pathogen and colorschemes, it adds vimrc entries in
``.vimp/vimrc``. This is read by adding a few lines to your
``~/.vimrc``. (I know, touching ``.vimrc`` is not cool, but I'll change
that later on).

Flags to vimp
-------------

-  ``vimp -h`` or ``vimp --help`` to print help.
-  ``vimp -V`` or ``vimp --version`` to print version.
-  ``vimp -v <command> [argument(s)]`` to print all actions performed,
   e.g. ``vimp -v install fuzzyfind``.

Commands
--------

-  ``vimp help`` to print help.
-  ``vimp help list`` to print help on the command ``list``.
-  ``vimp install <package(s)>`` to install packages.
-  ``vimp list`` to list installed packages
-  ``vimp list -a`` to list all available packages\`
-  ``vimp list <package(s)>`` to list package details.
-  ``vimp disable <package(s)>`` to disable packages, but leave on disk.
-  ``vimp remove <package(s)>`` to disable and delete packages.
-  ``vimp version`` to print version.

Aliases
-------

I haven't decided on the exact command names yet, so I have several
aliases so I can see which ones I like:

-  ``vimp ls`` is an alias for ``vimp list``
-  ``vimp get`` is an alias for ``vimp install``
-  ``vimp add`` is another alias for ``vimp install``
-  ``vimp find`` is an alias for ``vimp search``
-  ``vimp rm`` is an alias for ``vimp remove``
-  ``vimp uninstall`` is an alias for ``vimp disable``

Unimplemented commands
----------------------

-  ``vimp update`` to update the list of available packages.
-  ``vimp upgrade`` to actually upgrade packages with newer versions.

Requirements
------------

You need Python and vim, of course. It relies on Pathogen, but will
install this by default if it can't find it.

Installation
------------

I haven't made any installer yet, so you have to clone this project and
add the vimp path to ``$PATH``. On my system, I've added ``~/bin`` to my
``$PATH``, so I just symlink ``~/bin/vimp`` to ``~/devel/vimp/vimp``:

::

    $ git clone https://github.com/cslarsen/vimp
    $ cd vimp
    $ python setup.py install

Later, when vimp is more mature, I'll make it possible to install via
``pip``.

Adding new plugins / installations scripts to vimp
--------------------------------------------------

You can add new scripts to vimp by modifying ``scripts.py``. I won't
explain in detail how to now, but just look at what's there already.

If you *do* add new scripts that work, please send a patch to me.

To do
-----

There is a lot of stuff missing, and many corner cases that I don't
handle. However, I don't consider it dangerous to use vimp. In fact, I
feel it's rather quite safe.

Anyway, how much I will work on vimp depends on how many people can help
me with patches. Currently, it works pretty well for me.

Most glaringly, I don't have support for updating whatsoever.

List of various todos:

-  Add support for updating, upgrading
-  Do not leave behind dependencies when uninstalling
-  etc.

Bugs
----

There are many bugs. Please help me fix them!

In particular, globbing for extracting files doesn't work well.

License
-------

Copyright (C) 2014 Christian Stigen Larsen

Distributed under the LGPL v2.1, LGPL 3.0, GPL 2.0 or GPL 3.0.
