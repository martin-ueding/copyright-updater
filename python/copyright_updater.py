#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>


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
