"""
Simple logging facility.

Copyright (C) 2014 Christian Stigen Larsen
Distributed under the LGPL v2.1; see LICENSE.txt
"""

VERBOSE = False

def setverbose(flag):
    """Turn verbose logging on or off."""
    global VERBOSE
    VERBOSE = flag

def verb(*s):
  """If verbose mode is on, print a line to standard output."""
  if VERBOSE:
    print(" ".join(s))
