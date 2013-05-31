WebDriver Plus
==============

[![Build Status](https://secure.travis-ci.org/tomchristie/webdriverplus.png?branch=0.2.0)](http://travis-ci.org/tomchristie/webdriverplus)

The most simple and powerful way to use Selenium with Python
------------------------------------------------------------

WebDriver Plus is an extension to the Python bindings for Selenium WebDriver,
which gives you a more concise and expressive API.

It helps you to quickly write readable, robust tests.

What's so great about WebDriver Plus?

* Browser instances that support pooling and automatic quit on exit.
* A concise API for finding elements, and a wide range of selectors.
* JQuery-style traversal and filtering for locating elements without using
  complex xpath expressions.
* Perform actions on elements without having to use ActionChains.
* Element highlighting makes working from the Python console a joy.

**Note**: If you're interested in helping maintain WebDriver Plus in the long term please get in touch.  Most of the author's open source time is currently devoted to working on [Django REST framework][django-rest-framework].

Getting started
---------------

Install `webdriverplus` using `pip`.

    pip install webdriverplus

Now fire up your Python console...

    >>> from webdriverplus import WebDriver
    >>> browser = WebDriver().get('http://www.google.com')

Ok, let's do a search.

    >>> browser.find(name='q').send_keys('selenium\n')

Now let's get the headings for all the search results.

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
selecting the correct elements:

![image](https://raw.github.com/tomchristie/webdriverplus/master/docs/screenshot.png)

**IMPORTANT**: Breaking changes in 0.2.0
----------
Mainly methods that cause conflicts with the native Python WebDriver will be removed. Also methods with duplicate functionalities will be removed also.

- `id` property is no longer supported due to conflict with native Python WebDriver. You can use `attr('id')` instead.
- `is_checked`, `is_displayed`, `is_enabled` and `is_selected` will be methods instead of properties (so `is_checked()`, `is_displayed()`, `is_enabled()` and `is_selected()`)
- `style` property will be removed. You can use `css(name, value)` to get/set css properties

Next steps
----------

When you're ready to get going, head over to the
[full documentation](http://webdriver-plus.readthedocs.org/).

If you want to help contribute to the project, please read the
[contribution notes](http://webdriver-plus.readthedocs.org/en/latest/topics/contributing.html).

[django-rest-framework]: http://django-rest-framework.org/