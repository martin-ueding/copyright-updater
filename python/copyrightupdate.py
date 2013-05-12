#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2013 K Richard Pixley <rich@noir.com>

"""Parses the given lines and updates the copyright string.

Say you have a copyright string in the top of some source file, like::

    # Copyright (c) 2010 John Doe <john@example.com>

If you edit this file, you would like the copyright notice so reflect the
current year as well, like::

    # Copyright (c) 2010, 2012 John Doe <john@example.com>

This module checks for outdated copyright strings and updates them.

Ranges are detected and collapsed intelligently. If you have ``2008, 2009,
2010``, it will become ``2008-2010``. If you mix ranges and single years, this
will also be picked up correctly::

    2002, 2003, 2004, 2006, 2008, 2009, 2012

That list becomes::

    2002-2004, 2006, 2008-2009, 2012

In order to prevent changing of copyright notices that do not carry your name,
you can create an INI style configuration file at
``~/.config/copyright_updater.ini`` which would look like that:

.. code:: ini

    [copyrightupdate]
    linelimit = 6
    name = John Doe
    symbol-style = ©
    year = 1999
    warn = yes

Additionally, you can limit the search depth into the file by setting a number
of lines in linelimit.  This can be a time saver in some cases but may also
mean that some files won't get their copyrights updated if the copyright lines
are deep into the file.

It can replace any of the standard copyright symbols, ``(c)``, ``(C)``, or
``©`` with any arbitrary string automatically, if you set the symbol-style
option in the config file.  You can use this to force all updated copyrights to
use any particular style of symbol or even to remove the symbol altogether by
setting it to an empty string.

You can set a particular year if you need to, for instance, update files on
January 1 to represent the changes you made the day before.

And finally, if you set warn, the module will complain about any files for
which a suitable copyright line cannot be found.  This can happen if, for
instance, you have linelimit set too low or if you are the second copyright
owner of a file and have not yet added your own line to the file.
"""

import platform
if platform.python_version_tuple()[0] == '3':
    import configparser
else:
    import ConfigParser as configparser

import datetime
import os.path
import re
import logging

__docformat__ = "restructuredtext en"

logger = logging.getLogger(__name__)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

def suckfile(name):
    if platform.python_version_tuple()[0] == '3':
        with open(name, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    else:
        with open(name, 'r') as f:
            lines = f.readlines()

    return lines

def spitfile(name, lines):
    # go through -new so that if we're interrupted or crash while writing,
    # the file isn't lost.  The rename here is atomic so either the full
    # old file will exist at this name or the full new file will.
    new = name + '-new'

    if platform.python_version_tuple()[0] == '3':
        with open(new, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    else:
        with open(new, 'w') as f:
            f.writelines(lines)

    os.rename(new, name)


class ParamBlock:
    """
    Wraps the various parameters we might collect from a command line or a configfile.
    """

    def __init__(self, linelimit=0, name="", symbol_style=None, year=None, warn=False):
        self.linelimit = linelimit
        self.name = name
        self.symbol_style = symbol_style
        self.year = year if year else datetime.date.today().year
        self.warn = warn

        self.recompile()

    def __repr__(self):
        return '<{0}@{1}: linelimit = {2}, name = \'{3}\', symbol_style = \'{4}\', year = {5}, warn = {6}'.format(
            self.__class__.__name__, hex(id(self)), self.linelimit, self.name, self.symbol_style, self.year, self.warn)

    def __eq__(self, other):
        return (
            self.linelimit == other.linelimit
            and self.name == other.name
            and self.symbol_style == other.symbol_style
            and self.year == other.year
            and self.warn == other.warn
        )

    def regex(self):
        regex = '.*Copyright\D+(\d[0-9-, ]+\d)\D+'

        if self.name:
            regex += self.name

        return regex

    def recompile(self):
        self.pattern = re.compile(self.regex())

    _section_name = "copyrightupdate"

    def read(self, configfile=None):
        """
        Create a new ParamBlock from a configfile.  If the pb argument is
        given, it is overlaid with the configfile data.

        :param configfile: Filename to process
        :type f: str
        :param pb: existing ParamBlock to overlay
        :type pb: ParamBlock
        :rtype: ParamBlock
        """

        if configfile is None:
            configfile = os.path.expanduser("~/.config/copyright_updater.ini")

        if os.path.isfile(configfile):
            parser = configparser.ConfigParser()
            parser.read(configfile)

            if parser.has_section(self._section_name):
                if parser.has_option(self._section_name, "linelimit"):
                    self.linelimit = parser.getint(self._section_name, "linelimit")

                if parser.has_option(self._section_name, "name"):
                    self.name = parser.get(self._section_name, "name")

                if parser.has_option(self._section_name, "symbol-style"):
                    self.symbol_style = parser.get(self._section_name, "symbol-style")

                if parser.has_option(self._section_name, "year"):
                    self.year = parser.getint(self._section_name, "year")

                if parser.has_option(self._section_name, "warn"):
                    self.warn = parser.getboolean(self._section_name, "warn")

        self.recompile()
        return self

    def write(self, configfile=None):
        if not configfile:
            return

        parser = configparser.ConfigParser()
        parser.add_section(self._section_name)

        if self.linelimit:
            parser.set(self._section_name, 'linelimit', str(self.linelimit))

        if self.name:
            parser.set(self._section_name, 'name', self.name)

        if self.symbol_style:
            parser.set(self._section_name, 'symbol-style', self.symbol_style)

        if self.year:
            parser.set(self._section_name, 'year', str(self.year))

        if self.warn:
            parser.set(self._section_name, 'warn', 'yes' if self.warn else 'no')

        with open(configfile, 'w') as ofile:
            parser.write(ofile)

def process_file(f, pb):
    """
    Processes a single file.

    :param f: Filename to process
    :type f: str
    :param linecount: Up to which line should be processed.
    :type linecount: int
    """

    lines = suckfile(f)

    line_found, change_made = process_lines(lines, pb=pb)

    if pb.warn and not line_found:
        logger.warn('No suitable copyright line found for \'{0}\''.format(f))

    if change_made:
        spitfile(f, lines)

symbol_pattern = re.compile('(\([cC]\)|©)')

def process_lines(lines, pb):
    """
    Process the given lines.  Returns a tuple.  The first element of the tuple
    is True iff a relevant copyright line was found.  The second element of the
    tuple is True iff a change was made.  Even if a relevant line was found,
    there may be no change if the line already contains the year in question.

    :param lines: List of lines. This will be changed.
    :type lines: list
    :param pb: params
    :type pb: ParamBlock
    :rtype: Boolean

    """
    change_made = False

    linelimit = pb.linelimit if pb.linelimit else len(lines)

    copyright_years_string, linenumber = find_copyright_years_string(lines[:linelimit], pb=pb)

    if copyright_years_string is None:
        return (False, False)

    years = parse_years(copyright_years_string)

    if len(years) == 0:
        return (True, False)

    # If the year is not already in the list, append it and update the
    # line accordingly.
    if pb.year not in years:
        years.append(pb.year)
        joined_years = join_years(years)
        lines[linenumber] = re.sub(r"\d[0-9-, ]+\d", joined_years, lines[linenumber], count=1)
        change_made |= True

    if pb.symbol_style:
        lines[linenumber] = symbol_pattern.sub(pb.symbol_style, lines[linenumber], 1)
        change_made |= True

    return (True, change_made)

def find_copyright_years_string(lines, pb):
    """
    Find the copyright year string in a file.

    :param lines: Lines to process.
    :type lines: list
    :param linecount: Up to which line should be processed.
    :type linecount: int
    :return: Year string and line number.
    :rtype: tuple
    """
    for line, linenumber in zip(lines, range(len(lines))):
        match = pb.pattern.match(line)
        if match is not None:
            return match.group(1).strip(), linenumber

    return None, -1


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
        year_group = [int(x) for x in year_group]

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
