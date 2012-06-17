#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

###############################################################################
#                                   License                                   #
###############################################################################
# This file is part of copyright updater.
#
# copyright updater is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# copyright updater is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# copyright updater.  If not, see <http://www.gnu.org/licenses/>.

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
