#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2013 K Richard Pixley <rich@noir.com>

import unittest
import datetime
import os
import subprocess
import sys
import copy

import copyrightupdate

__docformat__ = "restructuredtext en"

current_year = datetime.date.today().year
configfile = 'configfile'
testfile = 'testfile'

def command_line_from_pb(pb):
    retval = [sys.executable, './copyright-updater']

    if pb.linelimit:
        retval += ['-l', '{0}'.format(pb.linelimit)]

    if pb.name:
        retval += ['-n', '{0}'.format(pb.name)]

    if pb.symbol_style:
        retval += ['-s', '{0}'.format(pb.symbol_style)]

    if pb.year:
        retval += ['-y', '{0}'.format(pb.year)]

    if pb.warn:
        retval += ['-w']

    retval.append(testfile)
    return retval

class CopyrightUpdaterTest(unittest.TestCase):
    def tearDown(self):
        try:
            os.remove(configfile)
        except:
            pass

        try:
            os.remove(testfile)
        except:
            pass

    def test_join_years(self):
        self.assertEquals(copyrightupdate.join_years([2002, 2003]), '2002-2003')
        self.assertEquals(copyrightupdate.join_years([2002, 2003, 2004]), '2002-2004')
        self.assertEquals(copyrightupdate.join_years([2002, 2004]), '2002, 2004')
        self.assertEquals(copyrightupdate.join_years([2002, 2003, 2004, 2008, 2009, 2012]), '2002-2004, 2008-2009, 2012')
        self.assertEquals(copyrightupdate.join_years([2002, 2003, 2004, 2006, 2008, 2009, 2012]), '2002-2004, 2006, 2008-2009, 2012')
        self.assertEquals(copyrightupdate.join_years([2002, 2004, 2003, 2008, 2012, 2009]), '2002-2004, 2008-2009, 2012')

    def test_parse_years(self):
        self.assertEquals(copyrightupdate.parse_years("2002"), [2002])
        self.assertEquals(copyrightupdate.parse_years("2002-2004"), [2002, 2003, 2004])
        self.assertEquals(copyrightupdate.parse_years("2002, 2004"), [2002, 2004])
        self.assertEquals(copyrightupdate.parse_years("2002-2004, 2010"), [2002, 2003, 2004, 2010])

    def filetest(self, lines, gold, pb):
        copyrightupdate.write_file(testfile, lines)
        subprocess.check_call(command_line_from_pb(pb))
        post = copyrightupdate.load_file(testfile)
        self.assertEquals(post, gold)

    # first series with default pb.

    def test_find_copyright_years_string_1(self):
        pb = copyrightupdate.ParamBlock()
        pb.write(configfile)

        pb2 = copyrightupdate.ParamBlock().read(configfile)
        self.assertEquals(pb, pb2)

        orig_lines = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "# Copyright © 2011 John Doe <john@example.com>\n",
            "# Copyright (c) 2010 Alpha Bravo AB.\n",
            "# Copyright (C) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        gold = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "# Copyright © 2011, {0} John Doe <john@example.com>\n".format(current_year),
            "# Copyright (c) 2010 Alpha Bravo AB.\n",
            "# Copyright (C) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        lines = copy.copy(orig_lines)

        years, line_number = copyrightupdate.find_copyright_years_string(lines, pb)

        self.assertEquals(years, "2011")
        self.assertEquals(line_number, 2)
            
        self.assertTrue(copyrightupdate.process_lines(lines, pb))
        self.assertEquals(lines, gold)

        lines = copy.copy(orig_lines)
        self.filetest(lines, gold, pb)

    def test_find_copyright_years_string_2(self):
        pb = copyrightupdate.ParamBlock()

        orig_lines = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (c) 2007-2009, 2011-2012 John Doe <john@example.com>\n",
            "# Copyright (C) 2010 Alpha Bravo AB.\n",
            "# Copyright © 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        gold = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (c) 2007-2009, 2011-{0} John Doe <john@example.com>\n".format(current_year),
            "# Copyright (C) 2010 Alpha Bravo AB.\n",
            "# Copyright © 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        lines = copy.copy(orig_lines)
        years, line_number = copyrightupdate.find_copyright_years_string(lines, pb)

        self.assertEquals(years, "2007-2009, 2011-2012")
        self.assertEquals(line_number, 3)

        self.assertTrue(copyrightupdate.process_lines(lines, pb))

        self.assertEquals(lines, gold)

        lines = copy.copy(orig_lines)
        self.filetest(lines, gold, pb)

    def test_process_lines(self):
        pb = copyrightupdate.ParamBlock()

        orig_lines = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (C) 2007-2009, 2011 John Doe <john@example.com>\n",
            "# Copyright © 2010 Alpha Bravo AB.\n",
            "# Copyright (c) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        gold = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (C) 2007-2009, 2011, {0} John Doe <john@example.com>\n".format(current_year),
            "# Copyright © 2010 Alpha Bravo AB.\n",
            "# Copyright (c) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        lines = copy.copy(orig_lines)
        years, line_number = copyrightupdate.find_copyright_years_string(lines, pb)
        self.assertEquals(years, "2007-2009, 2011")
        self.assertEquals(line_number, 3)

        self.assertTrue(copyrightupdate.process_lines(lines, pb))

        self.assertEquals(lines, gold)

        lines = copy.copy(orig_lines)
        self.filetest(lines, gold, pb)

    # second series with symbol-style set, (pbs)

    def test_pbs_find_copyright_years_string_1(self):
        pb = copyrightupdate.ParamBlock(symbol_style='@')
        pb.write(configfile)

        pb2 = copyrightupdate.ParamBlock().read(configfile)
        self.assertEquals(pb, pb2)

        orig_lines = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "# Copyright © 2011 John Doe <john@example.com>\n",
            "# Copyright (c) 2010 Alpha Bravo AB.\n",
            "# Copyright (C) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        gold = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "# Copyright @ 2011, {0} John Doe <john@example.com>\n".format(current_year),
            "# Copyright (c) 2010 Alpha Bravo AB.\n",
            "# Copyright (C) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        lines = copy.copy(orig_lines)
        years, line_number = copyrightupdate.find_copyright_years_string(lines, pb)

        self.assertEquals(years, "2011")
        self.assertEquals(line_number, 2)
            
        self.assertTrue(copyrightupdate.process_lines(lines, pb))

        self.assertEquals(lines, gold)

        lines = copy.copy(orig_lines)
        self.filetest(lines, gold, pb)

    def test_pbs_find_copyright_years_string_2(self):
        pb = copyrightupdate.ParamBlock(symbol_style='@')

        orig_lines = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (c) 2007-2009, 2011-2012 John Doe <john@example.com>\n",
            "# Copyright (C) 2010 Alpha Bravo AB.\n",
            "# Copyright © 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        gold = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright @ 2007-2009, 2011-{0} John Doe <john@example.com>\n".format(current_year),
            "# Copyright (C) 2010 Alpha Bravo AB.\n",
            "# Copyright © 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        lines = copy.copy(orig_lines)
        years, line_number = copyrightupdate.find_copyright_years_string(lines, pb)

        self.assertEquals(years, "2007-2009, 2011-2012")
        self.assertEquals(line_number, 3)

        self.assertTrue(copyrightupdate.process_lines(lines, pb))

        self.assertEquals(lines, gold)

        lines = copy.copy(orig_lines)
        self.filetest(lines, gold, pb)

    def test_pbs_process_lines(self):
        pb = copyrightupdate.ParamBlock(symbol_style='@')

        orig_lines = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (C) 2007-2009, 2011 John Doe <john@example.com>\n",
            "# Copyright © 2010 Alpha Bravo AB.\n",
            "# Copyright (c) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        gold = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright @ 2007-2009, 2011, {0} John Doe <john@example.com>\n".format(current_year),
            "# Copyright © 2010 Alpha Bravo AB.\n",
            "# Copyright (c) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        lines = copy.copy(orig_lines)
        years, line_number = copyrightupdate.find_copyright_years_string(lines, pb)
        self.assertEquals(years, "2007-2009, 2011")
        self.assertEquals(line_number, 3)

        self.assertTrue(copyrightupdate.process_lines(lines, pb))

        self.assertEquals(lines, gold)

        lines = copy.copy(orig_lines)
        self.filetest(lines, gold, pb)

    # third series with a name set, (pbn)

    def test_pbn_find_copyright_years_string_1(self):
        pb = copyrightupdate.ParamBlock(name="Alpha Bravo")
        pb.write(configfile)

        pb2 = copyrightupdate.ParamBlock().read(configfile)
        self.assertEquals(pb, pb2)

        orig_lines = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "# Copyright © 2011 John Doe <john@example.com>\n",
            "# Copyright (c) 2010 Alpha Bravo AB.\n",
            "# Copyright (C) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        gold = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "# Copyright © 2011 John Doe <john@example.com>\n",
            "# Copyright (c) 2010, {0} Alpha Bravo AB.\n".format(current_year),
            "# Copyright (C) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        lines = copy.copy(orig_lines)
        years, line_number = copyrightupdate.find_copyright_years_string(lines, pb)

        self.assertEquals(years, "2010")
        self.assertEquals(line_number, 3)
            
        self.assertTrue(copyrightupdate.process_lines(lines, pb))

        self.assertEquals(lines, gold)

        lines = copy.copy(orig_lines)
        self.filetest(lines, gold, pb)

    def test_pbn_find_copyright_years_string_2(self):
        pb = copyrightupdate.ParamBlock(name="Alpha Bravo")

        orig_lines = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (c) 2007-2009, 2011-2012 John Doe <john@example.com>\n",
            "# Copyright (C) 2010 Alpha Bravo AB.\n",
            "# Copyright © 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        gold = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (c) 2007-2009, 2011-2012 John Doe <john@example.com>\n",
            "# Copyright (C) 2010, {0} Alpha Bravo AB.\n".format(current_year),
            "# Copyright © 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        lines = copy.copy(orig_lines)
        years, line_number = copyrightupdate.find_copyright_years_string(lines, pb)

        self.assertEquals(years, "2010")
        self.assertEquals(line_number, 4)

        self.assertTrue(copyrightupdate.process_lines(lines, pb))

        self.assertEquals(lines, gold)

        lines = copy.copy(orig_lines)
        self.filetest(lines, gold, pb)

    def test_pbn_process_lines(self):
        pb = copyrightupdate.ParamBlock(name="Alpha Bravo")

        orig_lines = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (C) 2007-2009, 2011 John Doe <john@example.com>\n",
            "# Copyright © 2010 Alpha Bravo AB.\n",
            "# Copyright (c) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        gold = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (C) 2007-2009, 2011 John Doe <john@example.com>\n",
            "# Copyright © 2010, {0} Alpha Bravo AB.\n".format(current_year),
            "# Copyright (c) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        lines = copy.copy(orig_lines)
        years, line_number = copyrightupdate.find_copyright_years_string(lines, pb)
        self.assertEquals(years, "2010")
        self.assertEquals(line_number, 4)

        self.assertTrue(copyrightupdate.process_lines(lines, pb))

        self.assertEquals(lines, gold)

        lines = copy.copy(orig_lines)
        self.filetest(lines, gold, pb)

    # ...with a linelimit, (pdl)

    def test_pbl_find_copyright_years_string_1(self):
        pb = copyrightupdate.ParamBlock(linelimit=1)
        pb.write(configfile)

        pb2 = copyrightupdate.ParamBlock().read(configfile)
        self.assertEquals(pb, pb2)

        orig_lines = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "# Copyright © 2011 John Doe <john@example.com>\n",
            "# Copyright (c) 2010 Alpha Bravo AB.\n",
            "# Copyright (C) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        gold = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "# Copyright © 2011 John Doe <john@example.com>\n",
            "# Copyright (c) 2010 Alpha Bravo AB.\n",
            "# Copyright (C) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        lines = copy.copy(orig_lines)
        years, line_number = copyrightupdate.find_copyright_years_string(lines[:pb.linelimit], pb)

        self.assertEquals(years, None)
        self.assertEquals(line_number, -1)
            
        self.assertFalse(copyrightupdate.process_lines(lines, pb)[0])

        self.assertEquals(lines, gold)

        lines = copy.copy(orig_lines)
        self.filetest(lines, gold, pb)

    def test_pbl_find_copyright_years_string_2(self):
        pb = copyrightupdate.ParamBlock(linelimit=1)

        orig_lines = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (c) 2007-2009, 2011-2012 John Doe <john@example.com>\n",
            "# Copyright (C) 2010 Alpha Bravo AB.\n",
            "# Copyright © 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        gold = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (c) 2007-2009, 2011-2012 John Doe <john@example.com>\n",
            "# Copyright (C) 2010 Alpha Bravo AB.\n",
            "# Copyright © 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        lines = copy.copy(orig_lines)
        years, line_number = copyrightupdate.find_copyright_years_string(lines[:pb.linelimit], pb)

        self.assertEquals(years, None)
        self.assertEquals(line_number, -1)

        self.assertFalse(copyrightupdate.process_lines(lines, pb)[0])

        self.assertEquals(lines, gold)

        lines = copy.copy(orig_lines)
        self.filetest(lines, gold, pb)

    def test_pbl_process_lines(self):
        pb = copyrightupdate.ParamBlock(linelimit=1)

        orig_lines = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (C) 2007-2009, 2011 John Doe <john@example.com>\n",
            "# Copyright © 2010 Alpha Bravo AB.\n",
            "# Copyright (c) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        gold = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (C) 2007-2009, 2011 John Doe <john@example.com>\n",
            "# Copyright © 2010 Alpha Bravo AB.\n",
            "# Copyright (c) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        lines = copy.copy(orig_lines)
        years, line_number = copyrightupdate.find_copyright_years_string(lines[:pb.linelimit], pb)
        self.assertEquals(years, None)
        self.assertEquals(line_number, -1)

        self.assertFalse(copyrightupdate.process_lines(lines, pb)[0])

        self.assertEquals(lines, gold)

        lines = copy.copy(orig_lines)
        self.filetest(lines, gold, pb)

    # ...with a year, (pby)

    def test_pby_find_copyright_years_string_1(self):
        pb = copyrightupdate.ParamBlock(year=1999)
        pb.write(configfile)

        pb2 = copyrightupdate.ParamBlock().read(configfile)
        self.assertEquals(pb, pb2)

        orig_lines = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "# Copyright © 2011 John Doe <john@example.com>\n",
            "# Copyright (c) 2010 Alpha Bravo AB.\n",
            "# Copyright (C) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        gold = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "# Copyright © 1999, 2011 John Doe <john@example.com>\n",
            "# Copyright (c) 2010 Alpha Bravo AB.\n",
            "# Copyright (C) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        lines = copy.copy(orig_lines)
        years, line_number = copyrightupdate.find_copyright_years_string(lines[:pb.linelimit], pb)

        self.assertEquals(years, None)
        self.assertEquals(line_number, -1)
            
        self.assertTrue(copyrightupdate.process_lines(lines, pb))

        self.assertEquals(lines, gold)

        lines = copy.copy(orig_lines)
        self.filetest(lines, gold, pb)

    def test_pby_find_copyright_years_string_2(self):
        pb = copyrightupdate.ParamBlock(year=1999)

        orig_lines = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (c) 2007-2009, 2011-2012 John Doe <john@example.com>\n",
            "# Copyright (C) 2010 Alpha Bravo AB.\n",
            "# Copyright © 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        gold = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (c) 1999, 2007-2009, 2011-2012 John Doe <john@example.com>\n",
            "# Copyright (C) 2010 Alpha Bravo AB.\n",
            "# Copyright © 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        lines = copy.copy(orig_lines)
        years, line_number = copyrightupdate.find_copyright_years_string(lines[:pb.linelimit], pb)

        self.assertEquals(years, None)
        self.assertEquals(line_number, -1)

        self.assertTrue(copyrightupdate.process_lines(lines, pb))

        self.assertEquals(lines, gold)

        lines = copy.copy(orig_lines)
        self.filetest(lines, gold, pb)

    def test_pby_process_lines(self):
        pb = copyrightupdate.ParamBlock(year=1999)

        orig_lines = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (C) 2007-2009, 2011 John Doe <john@example.com>\n",
            "# Copyright © 2010 Alpha Bravo AB.\n",
            "# Copyright (c) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        gold = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (C) 1999, 2007-2009, 2011 John Doe <john@example.com>\n",
            "# Copyright © 2010 Alpha Bravo AB.\n",
            "# Copyright (c) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        lines = copy.copy(orig_lines)
        years, line_number = copyrightupdate.find_copyright_years_string(lines[:pb.linelimit], pb)
        self.assertEquals(years, None)
        self.assertEquals(line_number, -1)

        self.assertTrue(copyrightupdate.process_lines(lines, pb))

        self.assertEquals(lines, gold)

        lines = copy.copy(orig_lines)
        self.filetest(lines, gold, pb)

    # ...with warnings, (pbw)

    def test_pbw_find_copyright_years_string_1(self):
        pb = copyrightupdate.ParamBlock(warn=True)
        pb.write(configfile)

        pb2 = copyrightupdate.ParamBlock().read(configfile)
        self.assertEquals(pb, pb2)

        orig_lines = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "# Copyright © 2011 John Doe <john@example.com>\n",
            "# Copyright (c) 2010 Alpha Bravo AB.\n",
            "# Copyright (C) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        gold = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "# Copyright © 2011, 2013 John Doe <john@example.com>\n",
            "# Copyright (c) 2010 Alpha Bravo AB.\n",
            "# Copyright (C) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        lines = copy.copy(orig_lines)
        years, line_number = copyrightupdate.find_copyright_years_string(lines[:pb.linelimit], pb)

        self.assertEquals(years, None)
        self.assertEquals(line_number, -1)
            
        self.assertTrue(copyrightupdate.process_lines(lines, pb))

        self.assertEquals(lines, gold)

        lines = copy.copy(orig_lines)
        self.filetest(lines, gold, pb)

    def test_pbw_find_copyright_years_string_2(self):
        pb = copyrightupdate.ParamBlock(warn=True)

        orig_lines = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (c) 2007-2009, 2011-2012 John Doe <john@example.com>\n",
            "# Copyright (C) 2010 Alpha Bravo AB.\n",
            "# Copyright © 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        gold = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (c) 2007-2009, 2011-2013 John Doe <john@example.com>\n",
            "# Copyright (C) 2010 Alpha Bravo AB.\n",
            "# Copyright © 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        lines = copy.copy(orig_lines)
        years, line_number = copyrightupdate.find_copyright_years_string(lines[:pb.linelimit], pb)

        self.assertEquals(years, None)
        self.assertEquals(line_number, -1)

        self.assertTrue(copyrightupdate.process_lines(lines, pb))

        self.assertEquals(lines, gold)

        lines = copy.copy(orig_lines)
        self.filetest(lines, gold, pb)

    def test_pbw_process_lines(self):
        pb = copyrightupdate.ParamBlock(warn=True)

        orig_lines = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (C) 2007-2009, 2011 John Doe <john@example.com>\n",
            "# Copyright © 2010 Alpha Bravo AB.\n",
            "# Copyright (c) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        gold = [
            "#!/usr/bin/python\n",
            "# -*- coding: utf-8 -*-\n",
            "\n",
            "# Copyright (C) 2007-2009, 2011, 2013 John Doe <john@example.com>\n",
            "# Copyright © 2010 Alpha Bravo AB.\n",
            "# Copyright (c) 2009 <thingy@goodstuff.com>\n",
            "# eof\n",
        ]

        lines = copy.copy(orig_lines)
        years, line_number = copyrightupdate.find_copyright_years_string(lines[:pb.linelimit], pb)
        self.assertEquals(years, None)
        self.assertEquals(line_number, -1)

        self.assertTrue(copyrightupdate.process_lines(lines, pb))

        self.assertEquals(lines, gold)

        lines = copy.copy(orig_lines)
        self.filetest(lines, gold, pb)


if __name__ == '__main__':
    unittest.main()
