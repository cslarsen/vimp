try:
    from setuptools import setup
except ImportError:
    import sys
    print("You need setuptools to install vimp. This can be done with, e.g.")
    print("")
    print("    pip install setuptools")
    print("")
    sys.exit(1)

setup(
    name="vimp",
    version="0.0.1",
    author="Christian Stigen Larsen",
    author_email="csl@csl.name",
    keywords="vim",
    packages=["vimp", "vimp.test"],
    scripts=["bin/vimp"],
    url="https://github.com/cslarsen/vimp",
    license="LICENSE.txt",
    description="Command-line package manager or vim.",
    long_description=open("README.md").read(),
    zip_safe=True,
)
