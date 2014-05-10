#!/usr/bin/env python3

import re
from setuptools import setup, find_packages

version = re.search("^__version__\s*=\s*\"(.*)\"$",
  open("leprechaun/__init__.py").read(), re.M).group(1)

setup(
  name='leprechaun',
  version=version,
  description="A simple rainbow table generator",
  long_description=open("README.rst", encoding="utf-8").read(),
  author="Zach Dziura",
  author_email="zcdziura@gmail.com",
  url="https://github.com/zcdziura/leprechaun",
  license="MIT",
  packages=find_packages(),
  entry_points={
    "console_scripts": [
      "leprechaun = leprechaun.__main__:main"
    ]
  },
  classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Topic :: Security",
    "Topic :: Security :: Cryptography"
  ]
)
