.. _browsers:

Browser Instances
=================

Creating browser instances
--------------------------

To create a WebDriver browser instance:

.. code-block:: python

    from webdriverplus import WebDriver
    browser = WebDriver('firefox')

Currently supported browsers are ``firefox``, ``chrome``, ``ie``, ``htmlunit``, ``remote`` and ``phantomjs``.

The default browser is firefox.  If called without any arguments,
``WebDriver()`` will create a firefox instance.

.. code-block:: python

    browser = WebDriver()

reuse_browser
~~~~~~~~~~~~~

Because starting up a web browser instance on every test run can be a
significant performance hit, WebDriverPlus provides an easy way to allows
instances to be reused between test sessions.

Setting the ``reuse_browser`` flag ensures that when you call ``driver.quit()``
the browser will be returned to a browser pool, and reused when you create
a new WebBrowserInstance:

.. code-block:: python

    browser = WebDriver('firefox', reuse_browser=True)

There are some important aspects to bear in mind about this behaviour:

* WebDriver Plus currently has no way of clearing browser history or cache.
  Be aware that this may affect the behaviour of tests.
* On quitting the browser and returning it to the pool, WebDriver Plus
  will clear any cookies for the browser for the current domain.  It has
  no way of clearing all cookies for all domains.  If you have test cases
  that access URLs from multiple domains, consider if you need to explicitly
  clear any cookies between sessions.
* WebDriver Plus will only retain one instance of each browser type (Eg Firefox,
  Chrome etc...) in the pool.  Instances will only be reused if the arguments
  to the WebDriver() constructor have not changed since the previous instance
  was created.

quit_on_exit
~~~~~~~~~~~~

By default WebDriverPlus will ensure that when a python process quits
it will attempt to quit any remaining open WebDriver instances.

If you do not want this behaviour set quit_on_exit to False:

.. code-block:: python

    browser = WebDriver('firefox', quit_on_exit=False)

wait
~~~~

By default WebDriverPlus will not wait for elements to become available. You can
pass a ``wait`` argument to specify the number of seconds that ``find()`` should
wait for elements to become available before timing out.

.. code-block:: python

    browser = WebDriver('firefox', wait=10)

This uses WebDriverWait_ under the covers, but is much less verbose. The idea
behind setting a per-browser wait argument instead of forcing the programmer to
use ``WebDriverWait`` around each piece of code that needs to wait for an
element is to free the programmer from having to think about waiting, which
we consider a low-level detail that the framework should deal with.

.. _WebDriverWait: http://seleniumhq.org/docs/04_webdriver_advanced.html

highlight
~~~~

By default WebDriverPlus highlights elements it found. Setting highlight to falsy will disable this

Switching to an iframe
--------------------------

To switch to a specific iframe, call ``switch_to_frame()``

Waiting for a specific condition
--------------------------

Right now ``webdriverplus`` supports expected condition style waiting with ``wait_for(selector, displayed=True``.
By default it will wait until the element with ``selector`` to be present AND visible. If ``displayed`` is set to
False, it will only wait until element is present.

.. code-block:: python

    browser.wait_for('div')

Quitting browser instances
--------------------------

To quit a WebDriver browser instance, call ``quit()``:

.. code-block:: python

    browser.quit()

force
~~~~~

Setting the ``force`` flag causes the browser instance to quit and ignore the
value of the ``reuse_browser`` flag.  The instance will be terminated and
will not be returned to the browser pool:

.. code-block:: python

    browser.quit(force=True)

Supported browsers
------------------

* Firefox - Should run out-of-the-box.
* Chrome - Install the `chrome driver <http://code.google.com/p/selenium/wiki/ChromeDriver>`_ first.
* IE - Install the `IE driver <http://code.google.com/p/selenium/wiki/InternetExplorerDriver>`_ first.
* HTMLUnit (headless browser) - should auto-install and run out-of-the-box.
* PhantomJS - Install `PhantomJS <http://phantomjs.org/download.html>`_ first.


Headless mode using Xvfb or Xvnc
--------------------------------

Using `pyvirtualdisplay <http://pypi.python.org/pypi/PyVirtualDisplay>`_, you
can run real browser instances in a virtual X framebuffer or VNC session. This
enables you to run Firefox or Chrome tests in headless mode, without having to
install HTMLUnit.

.. code-block:: bash

    $ pip install pyvirtualdisplay

You need to install either `Xvfb
<http://www.x.org/releases/X11R7.6/doc/man/man1/Xvfb.1.xhtml>`_ or `Xvnc
<http://xvnc.sourceforge.net/>`_ as a backend for `pyvirtualdisplay`.

To run the headless tests, use the ``--headless`` argument::

    $ python runtests.py --headless
    Running tests in headless mode.
    .........................................................
    ----------------------------------------------------------------------
    Ran 57 tests in 7.715s

    OK
