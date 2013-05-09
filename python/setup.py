#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

from distutils.core import setup

import copyrightupdate

__docformat__ = "restructuredtext en"

setup(
    author = "Martin Ueding",
    author_email = "dev@martin-ueding.de",
    classifiers = [
        "Environment :: Console",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python",
        "Topic :: Text Editors",

    ],
    description = "Updates copyright years.",
    download_url = "http://martin-ueding.de/download/copyright-updater/",
    license = "GPLv2+",
    long_description = copyrightupdate.__doc__,
    name = "copyrightupdate",
    py_modules = ["copyrightupdate"],
    scripts = ["copyright-updater"],
    url = "http://martin-ueding.de/projects/copyright-updater/",
    version = "1.1.4",
)
