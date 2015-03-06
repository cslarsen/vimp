try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="vimp",
    packages=["vimp"],
    version="0.1.0",
    author="Christian Stigen Larsen",
    author_email="csl@csl.name",
    keywords=["vim"],
    scripts=["bin/vimp"],
    url="https://github.com/cslarsen/vimp",
    download_url="https://github.com/cslarsen/vimp/tarball/0.1.0",
    license="https://www.gnu.org/licenses/lgpl-2.1.html",
    description="Command-line package manager or vim.",
    long_description=open("README.rst").read(),
    zip_safe=True,
    test_suite="vimp.test",
    platforms=["unix"],
)
