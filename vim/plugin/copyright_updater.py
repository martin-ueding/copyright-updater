#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012-2013 Martin Ueding <martin-ueding.de>

"""
Vim client to copyrightupdate.
"""

import vim

has_imported = False

try:
    import copyrightupdate
except ImportError:
    pass
else:
    has_imported = True

__docformat__ = "restructuredtext en"

def update_copyright():
    if has_imported:
        copyrightupdate.process_lines(vim.current.buffer, 5, copyrightupdate.load_config_regex())
