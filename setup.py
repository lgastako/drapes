#!/usr/bin/env python

import os
from setuptools import setup
from setuptools import find_packages


if __name__ == "__main__":
    setup(name="drapes",
          version="0.0.8",
          description="A lightweight ORM for the 'db' library.",
          author="John Evans",
          author_email="lgastako@gmail.com",
          url="https://github.com/lgastako/drapes",
          install_requires=["db"],
          packages=find_packages(),
          provides=["drapes"])
