try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="vimp",
    description="Command line package manager for the vim editor.",
    packages=["vimp"],
    version="0.1.4",
    author="Christian Stigen Larsen",
    author_email="csl@csl.name",
    keywords=["vim"],
    scripts=["bin/vimp"],
    url="https://github.com/cslarsen/vimp",
    download_url="https://github.com/cslarsen/vimp/tarball/0.1.4",
    license="https://www.gnu.org/licenses/lgpl-2.1.html",
    long_description=open("README.rst").read(),
    zip_safe=True,
    test_suite="vimp.test",
    platforms=["unix", "osx"],
    classifiers=[
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
