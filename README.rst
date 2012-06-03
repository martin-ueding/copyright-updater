#################
copyright updater
#################

Updates the copyright years in source code files.

Installation
============

Go into the ``python`` folder and install the Python modules. You can either
do it for all users:

.. code:: console

    # python setup.py install

Or just for yourself:

.. code:: console

    $ python setup.py install --user

Then copy the contents of the ``vim`` folder (that is ``plugin``) into your
``~/.vim`` folder. If you use Pathogen, you should copy the files into
``~/.vim/bundle/copyright_updater/plugin/``.

Then setup the config file in ``~/.config/copyright_updater.ini`` which would
look like that:

.. code:: ini

    [name]
    name = John Doe
    email = john@example.com
