#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

import unittest

import copyright_updater

class CopyrightUpdaterTest(unittest.TestCase):
    def test_join_years(self):
        assert copyright_updater.join_years([2002, 2003]) == '2002-2003'
        assert copyright_updater.join_years([2002, 2003, 2004]) == '2002-2004'
        assert copyright_updater.join_years([2002, 2004]) == '2002, 2004'
        assert copyright_updater.join_years([2002, 2003, 2004, 2008, 2009, 2012]) == '2002-2004, 2008-2009, 2012'
        assert copyright_updater.join_years([2002, 2003, 2004, 2006, 2008, 2009, 2012]) == '2002-2004, 2006, 2008-2009, 2012'
        assert copyright_updater.join_years([2002, 2004, 2003, 2008, 2012, 2009]) == '2002-2004, 2008-2009, 2012'

    def test_parse_years(self):
        assert copyright_updater.parse_years("2002") == [2002]
        assert copyright_updater.parse_years("2002-2004") == [2002, 2003, 2004]
        assert copyright_updater.parse_years("2002, 2004") == [2002, 2004]
        assert copyright_updater.parse_years("2002-2004, 2010") == [2002, 2003, 2004, 2010]
