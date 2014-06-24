"""
Provides a facade class to extract files from various archive formats.

Copyright (C) 2014 Christian Stigen Larsen
Distributed under the LGPL v2.1; see LICENSE.txt
"""

import contextlib
import os
import shutil
import tarfile
import zipfile

class ArchiveMember(object):
    def __init__(self, member, name, isdir):
        self._obj = member
        self.name = name
        self.isdir = isdir

    def __str__(self):
        return "<ArchiveMember isdir={} '{}'>".format(self.isdir, self.name)

class ZipArchive(object):
    """Extract files from zip file."""
    def __init__(self, path):
        self.zipfile = zipfile.ZipFile(path)

    def __enter__(self):
        return self

    def __exit__(self, ex, bt, a):
        self.close()

    def close(self):
        self.zipfile.close()

    @property
    def members(self):
        for m in self.zipfile.infolist():
            name = m.filename
            isdir = m.filename.endswith("/")
            yield ArchiveMember(m, name, isdir)

    @contextlib.contextmanager
    def open(self, member):
        f = self.zipfile.open(member._obj)
        yield f
        f.close()

    def extract(self, member, path):
        if not member.isdir:
            with self.open(member) as src:
                with file(path, "wb") as dst:
                    shutil.copyfileobj(src, dst)
        else:
            os.mkdir(path)

class TarArchive(object):
    """Extract files from tar file."""
    def __init__(self, path):
        self.tar = tarfile.open(path, "r")

    def __enter__(self):
        return self

    def __exit__(self, ex, bt, a):
        self.close()

    def close(self):
        self.tar.close()

    @property
    def members(self):
        for m in self.tar.getmembers():
            name = m.name
            isdir = m.isdir()
            yield ArchiveMember(m, name, isdir)

    def extract(self, member, path):
        if not member.isdir:
            obj = member._obj
            onlypath, filename = os.path.split(path)

            # Requested to change filename as well?
            if len(filename) > 0:
                obj.name = filename
                self.tar.extract(obj, onlypath)
            else:
                self.tar.extract(obj, path)
        else:
            os.mkdir(path)

class Archive(object):
    """Extract files form tar og zip file."""
    def __init__(self, path):
        if path.lower().endswith(".zip"):
            self.archive = ZipArchive(path)
        elif path.lower().endswith(".tar.gz"):
            self.archive = TarArchive(path)
        elif path.lower().endswith(".tar.bz2"):
            self.archive = TarArchive(path)
        elif path.lower().endswith(".tar"):
            self.archive = TarArchive(path)
        else:
            raise ValueError("Unknown type of archive file: %s" % path)

    def __enter__(self):
        return self

    def __exit__(self, ex, bt, a):
        self.close()

    def close(self):
        self.archive.close()

    @property
    def members(self):
        return self.archive.members

    def extract(self, member, path):
        self.archive.extract(member, path)
