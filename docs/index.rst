.. meta::
   :description: .
   :keywords: python, django, selenium, webdriver


WebDriver Plus
==============

The most elegant way to use Selenium with Python
------------------------------------------------

WedDriver Plus is an extension to the Python bindings for Selenium WebDriver,
which gives you a more concise and expressive API.

It helps you to quickly write readable, robust tests.

What's so great about WebDriver Plus?

* Browser instances that support pooling and automatic quit on exit.
* A concise API for finding elements, and a wide range of selectors.
* JQuery-style traversal and filtering for locating elements without using
  complex xpath expressions.
* Perform actions on elements without having to use ActionChains.
* Element highlighting makes working from the Python console a joy.

.. note::
    WebDriver Plus is not yet ready for use.
    It is in active development.
    Contributions welcome!

Getting started
---------------

Install ``webdriverplus`` using ``pip``.

.. code-block:: bash

    pip install webdriverplus

Now fire up your Python console...

.. code-block:: python

    >>> from webdriverplus import WebDriver
    >>> browser = WebDriver().get('http://www.google.com')

Ok, let's do a search.

.. code-block:: python

    >>> browser.find(name='q').send_keys('selenium\n')

Now let's get the headings for all the search results.

.. code-block:: python

    >>> browser.find(id='search').find('h3')
    WebElementSet(
      <h3 class="r"><a href="http://seleniumhq.org/" class="l" onmousedown="retur...
      <h3 class="r"><a href="http://www.google.co.uk/url?sa=t&amp;rct=j&amp;q=sel...
      <h3 class="r"><a href="http://en.wikipedia.org/wiki/Selenium" class="l" onm...
      <h3 class="r"><a href="http://en.wikipedia.org/wiki/Selenium_%28software%29...
      <h3 class="r"><a href="http://ods.od.nih.gov/factsheets/selenium" class="l"...
      <h3 class="r"><a href="http://www.nlm.nih.gov/medlineplus/druginfo/natural/...
      <h3 class="r"><a href="http://www.hollandandbarrett.com/selenium-050" class...
      <h3 class="r"><a href="http://www.whfoods.com/genpage.php?dbid=95&amp;tname...
      <h3 class="r"><a href="http://www.patient.co.uk/doctor/Selenium.htm" class=...
      <h3 class="r"><a href="/search?q=selenium&amp;hl=en&amp;biw=940&amp;bih=938...
      <h3 class="r"><a href="http://www.umm.edu/altmed/articles/selenium-000325.h...
    )

Notice that WebDriver Plus has highlighted the selected elements for you, which
is super helpful for when you're writing tests and trying to make sure you're
selecting the correct elements.

Overview
--------

.. toctree::
  :maxdepth: 1

  browsers
  selectors
  actions
  traversing
  filtering
  inspection

Topics
------

.. toctree::
  :maxdepth: 1

  topics/migrating
  topics/contributing

API Reference
-------------

.. toctree::
  :maxdepth: 1

  api/webdriver
  api/webelementset
