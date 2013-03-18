#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

from distutils.core import setup

__docformat__ = "restructuredtext en"

setup(
    author = "Martin Ueding",
    author_email = "dev@martin-ueding.de",
    description = "Updates copyright years.",
    name = "copyrightupdate",
    py_modules = ["copyrightupdate"],
    scripts = ["copyright-updater"],
    version = "1.1.1",
)
