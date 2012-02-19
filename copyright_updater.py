#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

"""
Parses the given files and updates the copyright string.

Say you have a copyright string in the top of some source file, like::

    # Copyright (c) 2010 John Doe <john@example.com>

If you edit this file, you would like the copyright notice so reflect the
current year as well, like::

    # Copyright (c) 2010, 2012 John Doe <john@example.com>

This script checks for outdated copyright strings and updates them.

Ranges are detected and collapsed intelligently. If you have C{2008, 2009,
2010}, it will become C{2008-2010}. If you mix ranges and single years, this
will also be picked up correctly::

    2002, 2003, 2004, 2006, 2008, 2009, 2012

That list becomes::

    2002-2004, 2006, 2008-2009, 2012

In order to prevent changing of copyright notices that do not carry your name,
you can create an INI style configuration file at
C{~/.config/copyright_updater.ini} which would look like that::

    [name]
    name = John Doe
    email = john@example.com

If no input files are given, the program acts as a filter from STDIN to STDOUT.
"""

import argparse
import ConfigParser
import datetime
import os.path
import re
import sys

def main():
    """
    Parses command line options and checks all given files.
    """
    options = _parse_args()

    if len(options.files) > 0:
        for f in options.files:
            # Ignore nonexistant files.
            if not os.path.isfile(f):
                continue

            process_file(f, options.linecount)

    else:
        lines = sys.stdin.readlines()

        if len(lines) > 0:
            process_lines(lines, len(lines))

            for line in lines:
                sys.stdout.write(line)




def process_file(f, linecount):
    """
    Processes a single file.

    @param f: Filename to process
    @type f: str
    @param linecount: Up to which line should be processed.
    @type linecount: int
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

    @param lines: Lines to process.
    @type lines: list
    @param linecount: Up to which line should be processed.
    @type linecount: int
    @return: Year string and line number.
    @rtype: tuple
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
    configfile = os.path.expanduser("~/.config/copyright_updater.ini")
    if os.path.isfile(configfile):
        parser = ConfigParser.ConfigParser()
        parser.read(configfile)

        if parser.has_option("name", "name"):
            name = parser.get("name", "name")
            if parser.has_option("name", "email"):
                email = "<%s>" % parser.get("name", "email")

                return name+".*"+email+".*"

    return ""


def parse_years(year_string):
    """
    Parses the year or years out of a string with years.

    >>> parse_years("2002-2004, 2010")
    [2002, 2003, 2004, 2010]

    @param year_string: String with years.
    @type year_string: str
    @return: List with every single year.
    @rtype: list
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

    @param years_list: List with every single year.
    @type years_list: list
    @return: Joined string.
    @rtype: str
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

    @param comma_groups: List with already collapsed ranges. This will be changed.
    @type comma_groups: list
    @param year_group: List with range to be collapsed.
    @type year_group: list
    """
    if len(year_group) == 1:
        comma_groups.append(str(year_group[0]))
    elif len(year_group) > 1:
        comma_groups.append("%d-%d" % (year_group[0], year_group[-1]))


def _parse_args():
    """
    Parses the command line arguments.

    @return: Namespace with arguments.
    @rtype: Namespace
    """
    parser = argparse.ArgumentParser(usage="%(prog)s [options] file ...", description="Updates the copyright dates in source code.")
    parser.add_argument('files', metavar='file', type=str, nargs='*',
                   help='Files to check.')
    parser.add_argument("-n", dest="linecount", type=int, default=5,
                        help="Number of lines to check from the beginning of the document.")
    parser.add_argument("--test", dest="test", action="store_true",
                        help="Perform doctests.")
    #parser.add_argument('--version', action='version', version='<the version>')

    return parser.parse_args()


if __name__ == "__main__":
    main()
