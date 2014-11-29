import os
from gittle import Gittle

def clone(url, path):
    """Clone a git repository from URL into local path.

    Returns:
        A Gittle repository.
    """
    return Gittle.clone(url, path)

def pull(path):
    """Update git repository by doing git pull.

    Returns:
        A Gittle repository.
    """
    repo = Gittle(path)
    repo.pull(origin_uri=repo.remotes["origin"])
    return repo

def clone_or_pull(url, path):
    """Clone git repository if it doesn't exist, or pull if it does."""
    if os.path.exists(path):
        pull(path)
    else:
        clone(url, path)
