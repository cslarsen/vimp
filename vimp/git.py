import os
from gittle import Gittle

from vimp.log import (verb)

def clone(url, path):
    """Clone a git repository from URL into local path.

    Returns:
        A Gittle repository.
    """
    verb("Cloning git repo repo %s to %s" % (url, path))
    return Gittle.clone(url, path)

def pull(path):
    """Update git repository by doing git pull.

    Returns:
        A Gittle repository.
    """
    verb("Pulling git repo at %s" % path)
    repo = Gittle(path)
    repo.pull(origin_uri=repo.remotes["origin"])
    return repo

def clone_or_pull(url, path):
    """Clone git repository if it doesn't exist, or pull if it does."""
    if os.path.exists(path):
        pull(path)
    else:
        clone(url, path)
