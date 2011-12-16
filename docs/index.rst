.. meta::
   :description: .
   :keywords: python, django, selenium, webdriver


WebDriver Plus
==============

WedDriver Plus is an extension to the Python wrapper for Selenium WebDriver.

It gives you a concise and expressive API, which lets you quickly write
readable, robust tests.

.. note::
    WebDriver Plus is not yet ready for use.
    It is in active development.
    Contributions welcome!

Getting started
---------------

Install ``webdriverplus`` using ``pip``.

.. code-block:: bash

    pip install webdriverplus

Now fire up your python console...

.. code-block:: python

    >>> import webdriverplus
    >>> driver = webdriverplus.Firefox()
    >>> driver.get('http://www.google.com')
    <WebDriver Instance, firefox>
    >>> driver.find('a')
    WebElementSet(
        ...
    )

    driver.find('a').filter(text='Images').click()


Contents
--------

.. toctree::
  :maxdepth: 1

  browsers
  selectors
  actions
  traversing
  filtering
  inspection

API Reference
-------------

.. toctree::
  :maxdepth: 1

  api/webdriver
  api/webelementset
