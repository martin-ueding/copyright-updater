#!/usr/bin/python
# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

from distutils.core import setup

setup(
    author = "Martin Ueding",
    author_email = "dev@martin-ueding.de",
    description = "Updates the year in copyright strings.",
    name = "copyright_updater",
    py_modules = ["copyright_updater"],
    scripts = ["copyright-updater"],
    version = "0.1",
)
