#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

import argparse
import re
import sys

def main():
    options = _parse_args()

    for f in options.files:
        process_file(f, options.linecount)


def process_file(f, linecount):
    copyright_years_string = find_copyright_years_string(f, linecount)

    if copyright_years_string is None:
        return

    years = parse_years(copyright_years_string)


def find_copyright_years_string(f, linecount):
    linenumber = 1

    pattern = re.compile(r".*Copyright\D+([0-9-, ]+)\D+.*")

    with open(f) as infile:
        for line in infile:
            match = pattern.match(line)
            if match is not None:
                return match.group(1).strip()

            linenumber += 1
            if linenumber > linecount:
                break

    return None


def parse_years(year_string):
    """
    Parses the year or years out of a string with years.

    >>> parse_years("2002")
    [2002]

    >>> parse_years("2002-2004")
    [2002, 2003, 2004]

    >>> parse_years("2002, 2004")
    [2002, 2004]

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

    return years


class YearParseException(Exception):
    pass


def _parse_args():
    """
    Parses the command line arguments.

    @return: Namespace with arguments.
    @rtype: Namespace
    """
    parser = argparse.ArgumentParser(usage="%(prog)s [options] file ...", description="Updates the copyright dates in source code.")
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                   help='Files to check.')
    parser.add_argument("-n", dest="linecount", type=int, default=5,
                        help="Number of lines to check from the beginning of the document.")
    parser.add_argument("--test", dest="test", action="store_true",
                        help="Perform doctests.")
    #parser.add_argument('--version', action='version', version='<the version>')

    return parser.parse_args()


if __name__ == "__main__":
    if "--test" in sys.argv:
        import doctest
        doctest.testmod()
        sys.exit(0)

    main()

