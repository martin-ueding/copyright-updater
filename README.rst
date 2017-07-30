.. Copyright © 2012, 2015, 2017 Martin Ueding <dev@martin-ueding.de>

#################
copyright-updater
#################

Updates the copyright years in source code files.

What It Does
============

Say you have a copyright string in the top of some source file, like::

    # Copyright © 2010 John Doe <john@example.com>

If you edit this file, you would like the copyright notice so reflect the
current year as well, like::

    # Copyright © 2010, 2012 John Doe <john@example.com>

This script checks for outdated copyright strings and updates them.

Ranges are detected and collapsed intelligently. If you have ``2008, 2009,
2010``, it will become ``2008-2010``. If you mix ranges and single years, this
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

    [unicode]
    replace = true

Additionally, it can replace ``(c)`` with ``©`` automatically, if you set the
option in the config file.

How To Use It
=============

There is a command line utility that you can use to update the copyright in
given files.

Then there is also a Vim plugin that checks your files every time you save a
file. That way, the copyright is always up to date.

- `Python Package Index page <https://pypi.python.org/pypi/copyrightupdate>`_

Installation
============

Makefile
--------

On Debian based systems, you can just call ``make install``. If you want other
options passed to ``./setup.py install``, then call ``make`` with a different
``setupoptions=…`` argument, where you can specify all the options that you
want to setuptools.

Manual
------

Go into the ``python`` folder and install the Python modules. You can either
do it for all users::

    python setup.py install

Or just for yourself::

    python setup.py install --user

Then copy the contents of the ``vim`` folder (that is ``plugin``) into your
``~/.vim`` folder. If you use Pathogen, you should copy the files into
``~/.vim/bundle/copyright_updater/plugin/``.
