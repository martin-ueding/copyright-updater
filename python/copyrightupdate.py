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
Parses the given lines and updates the copyright string.

Say you have a copyright string in the top of some source file, like::

    # Copyright (c) 2010 John Doe <john@example.com>

If you edit this file, you would like the copyright notice so reflect the
current year as well, like::

    # Copyright (c) 2010, 2012 John Doe <john@example.com>

This script checks for outdated copyright strings and updates them.

Ranges are detected and collapsed intelligently. If you have ``2008, 2009,
2010}, it will become ``2008-2010``. If you mix ranges and single years, this
will also be picked up correctly::

    2002, 2003, 2004, 2006, 2008, 2009, 2012

That list becomes::

    2002-2004, 2006, 2008-2009, 2012

In order to prevent changing of copyright notices that do not carry your name,
you can create an INI style configuration file at
``~/.config/copyright_updater.ini`` which would look like that::

    [name]
    name = John Doe
    email = john@example.com
"""

import ConfigParser
import datetime
import os.path
import re

__docformat__ = "restructuredtext en"

def process_file(f, linecount):
    """
    Processes a single file.

    :param f: Filename to process
    :type f: str
    :param linecount: Up to which line should be processed.
    :type linecount: int
    """

    lines = []
    with open(f) as orig:
        lines = orig.readlines()

    process_lines(lines, linecount, load_config_regex())

    with open(f, "w") as new:
        for line in lines:
            new.write(line)


def process_lines(lines, linecount, config_regex=""):
    """
    Process the given lines up to linecount.

    :param lines: List of lines. This will be changed.
    :type lines: list
    :param linecount: Up to which line should be searched.
    :type linecount: int
    :param config_regex: Additional RegEx to match for.
    :type config_regex: str
    """
    copyright_years_string, linenumber = find_copyright_years_string(lines, linecount, config_regex)

    if copyright_years_string is None:
        return

    years = parse_years(copyright_years_string)

    if len(years) == 0:
        return

    # Add the current year.
    d = datetime.date.today()

    # If the current year is already in the list, do nothing.
    if d.year in years:
        return

    years.append(d.year)

    joined_years = join_years(years)

    copyright_line = lines[linenumber]
    new_copyright_line = re.sub(r"\d[0-9-, ]+\d", joined_years, copyright_line, count=1)
    lines[linenumber] = new_copyright_line


def find_copyright_years_string(lines, linecount, config_regex=""):
    """
    Find the copyright year string in a file.

    :param lines: Lines to process.
    :type lines: list
    :param linecount: Up to which line should be processed.
    :type linecount: int
    :return: Year string and line number.
    :rtype: tuple
    """
    linenumber = 0

    pattern = re.compile(r".*Copyright\D+(\d[0-9-, ]+\d)\D+.*"+config_regex)

    for line in lines:
        match = pattern.match(line)
        if match is not None:
            return match.group(1).strip(), linenumber

        linenumber += 1
        if linenumber > linecount:
            break

    return None, -1


def load_config_regex():
    """
    Loads the regex that matches the name and email stored in the settings
    file.

    :return: RegEx.
    :rtype: str
    """
    configfile = os.path.expanduser("~/.config/copyright_updater.ini")
    if os.path.isfile(configfile):
        parser = ConfigParser.ConfigParser()
        parser.read(configfile)

        if parser.has_option("name", "name"):
            name = parser.get("name", "name")
            if parser.has_option("name", "email"):
                email = "<%s>" % parser.get("name", "email")

                return build_regex(name, email)

    return ""


def build_regex(name, email):
    """
    Build a regex that matches a name and email combination.

    >>> build_regex("John Doe", "john@example.com")
    'John Doe.*john@example.com.*'

    :param name: Name of the person.
    :type name: str
    :param email: Email of the person.
    :type email: str
    :return: RegEx.
    :rtype: str
    """
    return name+".*"+email+".*"


def parse_years(year_string):
    """
    Parses the year or years out of a string with years.

    >>> parse_years("2002-2004, 2010")
    [2002, 2003, 2004, 2010]

    :raise YearParseException: Raised if a range consists of more then two elements.
    :param year_string: String with years.
    :type year_string: str
    :return: List with every single year.
    :rtype: list
    """
    years = []

    comma_groups = re.split(r"\s*,\s*", year_string)

    for comma_group in comma_groups:
        year_group = re.split(r"\s*-\s*", comma_group)
        year_group = map(int, year_group)

        if len(year_group) == 1:
            years += year_group

        elif len(year_group) == 2:
            years += range(year_group[0], year_group[1]+1)

        else:
            raise YearParseException("Cannot parse %s" % comma_group)

    return sorted(years)


class YearParseException(Exception):
    """
    Exception if a year string cannot be parsed.
    """


def join_years(years_list):
    """
    Joins a list of years.

    It detects ranges and collapses them.

    >>> join_years([2002, 2003, 2004, 2006, 2008, 2009, 2012])
    '2002-2004, 2006, 2008-2009, 2012'

    :param years_list: List with every single year.
    :type years_list: list
    :return: Joined string.
    :rtype: str
    """
    years = sorted(set(years_list))

    comma_groups = []
    year_group = []
    for year in years:
        if len(year_group) > 0 and year - year_group[-1] > 1:
            _flush_group(comma_groups, year_group)
            year_group = []

        year_group.append(year)

    _flush_group(comma_groups, year_group)

    result = ', '.join(comma_groups)

    return result


def _flush_group(comma_groups, year_group):
    """
    Move the years in the year_group into the comma_groups.

    :param comma_groups: List with already collapsed ranges. This will be changed.
    :type comma_groups: list
    :param year_group: List with range to be collapsed.
    :type year_group: list
    """
    if len(year_group) == 1:
        comma_groups.append(str(year_group[0]))
    elif len(year_group) > 1:
        comma_groups.append("%d-%d" % (year_group[0], year_group[-1]))
