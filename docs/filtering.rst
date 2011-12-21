.. _filtering:

Filtering
=========

The `filter()` and `exclude()` methods can be used to filter the elements in
a WebElementSet.

filter(*selector*)
------------------

Filters the ``WebElementSet`` to only include elements that match the selector.

.. code-block:: python

    >>> from webdriverplus import WebDriver
    >>> snippet = """
    ... <ul>
    ...     <li>1</li>
    ...     <li class="selected">2</li>
    ...     <li>3</li>
    ...     <li>4</li>
    ...     <li class="selected">5</li>
    ... </ul>"""
    >>> elems = WebDriver().open(snippet).find('li').filter('.selected')
    WebElementSet(
      <li class="selected">2</li>
      <li class="selected">5</li>
    )

exclude(*selector*)
-------------------

Filters the ``WebElementSet`` to only include elements that do not match the
selector.

.. code-block:: python

    >>> from webdriverplus import WebDriver
    >>> snippet = """
    ... <ul>
    ...     <li>1</li>
    ...     <li class="selected">2</li>
    ...     <li>3</li>
    ...     <li>4</li>
    ...     <li class="selected">5</li>
    ... </ul>"""
    >>> WebDriver().open(snippet).find('li').exclude('.selected')
    WebElementSet(
      <li>1</li>
      <li>3</li>
      <li>4</li>
    )
