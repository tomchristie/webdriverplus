.. _contributing:

Contributing
============

WebDriver Plus is `hosted on GitHub <https://github.com/tomchristie/webdriverplus>`_,
and is currently in pre-release.

Contributions and bug reports are always welcome.

Requirements
------------

If you are using a git clone of the project, rather than a `pip install`,
you'll need to make sure you've installed ``selenium``.

``pip install selenium``

Running the Tests
-----------------

``./runtests.py``

There are also some slower tests which are not run by default.
To include these tests:

``./runtests.py --all``

Building the Docs
-----------------

``./makedocs.sh``
