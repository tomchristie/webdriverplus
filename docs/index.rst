.. meta::
   :description: .
   :keywords: python, django, selenium, webdriver


WebDriver Plus
==============

WedDriver Plus is a Python wrapper for Selenium WebDriver, that supports a
richer, more expressive API.


**A more concise, pythonic API**

``driver.find(id='searchbar')``, instead of ``driver.find_element_by_id('searchbar')``

**A rich set of selectors**

``driver.find(attribute='selected')``, ``driver.find(text='Welcome!')``...

**Chaining**

Eg. ``driver.find_all('li').click()``

**Tree traversal**

Eg. ``elem.children``, ``elem.next``, ``elem.siblings``...

**Shortcuts**

``elem.html``, ``elem.inner_html``

.. toctree::
  :maxdepth: 1

  forms
  selectors
  traversing
  actions
  inspection

**Inspection**

**Manipuation**

  jquery?
  javascript

**Filtering**

  .find
  .find_all
  .exists
  .filter
  .exclude

chaining ?


**SELECTORS: label_text, label_text_contains, selected=True/False, checked=True/False**
