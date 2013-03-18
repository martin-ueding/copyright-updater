#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

import unittest

import copyrightupdate

__docformat__ = "restructuredtext en"

class CopyrightUpdaterTest(unittest.TestCase):
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

    def test_find_copyright_years_string_1(self):
        lines = [
            "#!/usr/bin/python",
            "# -*- coding: utf-8 -*-",
            "# Copyright © 2011 John Doe <john@example.com>",
        ]

        years, line_number = copyrightupdate.find_copyright_years_string(
            lines, 5
        )

        self.assertEquals(years, "2011")
        self.assertEquals(line_number, 2)
            
    def test_find_copyright_years_string_2(self):
        lines = [
            "#!/usr/bin/python",
            "# -*- coding: utf-8 -*-",
            "",
            "# Copyright © 2007-2009, 2011-2012 John Doe <john@example.com>",
        ]

        years, line_number = copyrightupdate.find_copyright_years_string(
            lines, 5
        )

        self.assertEquals(years, "2007-2009, 2011-2012")
        self.assertEquals(line_number, 3)


    def test_process_lines(self):
        lines = [
            "#!/usr/bin/python",
            "# -*- coding: utf-8 -*-",
            "",
            "# Copyright © 2007-2009, 2011 John Doe <john@example.com>",
        ]

        copyrightupdate.process_lines(lines, 10)

        self.assertEquals(lines, [
            "#!/usr/bin/python",
            "# -*- coding: utf-8 -*-",
            "",
            "# Copyright © 2007-2009, 2011, 2013 John Doe <john@example.com>",
        ])
