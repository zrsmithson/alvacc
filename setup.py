#!/usr/bin/env python3

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


package_name = "alvacc"
source_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(source_dir, "requirements.txt")) as f:
    requirements = f.read().splitlines()

# Read in README.md for our long_description
with open(os.path.join(source_dir, "readme.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=package_name,
    description="Simple tool for querying Alabama vaccine website to check for available appointments",
    entry_points={
        "console_scripts": ["alvacc = alvacc.__main__:main"],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="1.0",
    install_requires=requirements,
    author="Zachary Smithson",
    author_email="zrsmithson@gmail.com",
    url="https://github.com/zrsmithson/alvacc",
    licence="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
)