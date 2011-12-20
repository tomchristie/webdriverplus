.. _traversing:

Traversing
==========

children
--------

Get the children of each element in the set of matched elements, optionally
filtered by a selector.

.. code-block:: python

    >>> from webdriverplus import WebDriver
    >>> snippet = """
    ... <ul>
    ...     <li>1</li>
    ...     <li><strong>2</strong></li>
    ...     <li>3</li>
    ... </ul>"""
    >>> WebDriver().open(snippet).find('ul').children
    WebElementSet(
      <li>1</li>
      <li><strong>2</strong></li>
      <li>3</li>
    )

parent
------

Get the parent of each element in the current set of matched elements,
optionally filtered by a selector.

.. code-block:: python

    >>> from webdriverplus import WebDriver
    >>> snippet = """
    ... <ul>
    ...     <li>1</li>
    ...     <li><strong>2</strong></li>
    ...     <li>3</li>
    ... </ul>"""
    >>> WebDriver().open(snippet).find('strong').parent
    WebElementSet(
      <li><strong>2</strong></li>
    )

descendants
-----------

Get the descendants of each element in the current set of matched elements.

.. code-block:: python

    >>> from webdriverplus import WebDriver
    >>> snippet = """
    ... <ul>
    ...     <li>1</li>
    ...     <li><strong>2</strong></li>
    ...     <li>3</li>
    ... </ul>"""
    >>> WebDriver().open(snippet).find('ul').descendants
    WebElementSet(
      <li>1</li>
      <li><strong>2</strong></li>
      <strong>2</strong>
      <li>3</li>
    )

.. note::

    Unlike the other traversal operations ``.descendants()`` cannot be
    filtered by a selector.  Use ``.find()`` instead.

ancestors
---------

Get the ancestors of each element in the current set of matched elements,
optionally filtered by a selector.

.. code-block:: python

    >>> from webdriverplus import WebDriver
    >>> snippet = """
    ... <ul>
    ...     <li>1</li>
    ...     <li class="selected">2</li>
    ...     <li>3</li>
    ... </ul>"""
    >>> WebDriver().open(snippet).find('.selected').parents
    WebElementSet(
      <html webdriver="true"><head></head><body><ul> <li>1</li> <li class="select...
      <body><ul> <li>1</li> <li class="selected">2</li> <li>3</li> </ul></body>
      <ul> <li>1</li> <li class="selected">2</li> <li>3</li> </ul>
    )

next
----

Get the immediately following sibling of each element in the set of matched
elements, optionally filtered by a selector.

.. code-block:: python

    >>> from webdriverplus import WebDriver
    >>> snippet = """
    ... <ul>
    ...     <li>1</li>
    ...     <li>2</li>
    ...     <li class="selected">3</li>
    ...     <li>4</li>
    ...     <li>5</li>
    ... </ul>"""
    >>> WebDriver().open(snippet).find('li.selected').next
    WebElementSet(
      <li>4</li>
    )

prev
----

Get the immediately preceding sibling of each element in the set of matched
elements, optionally filtered by a selector.

.. code-block:: python

    >>> from webdriverplus import WebDriver
    >>> snippet = """
    ... <ul>
    ...     <li>1</li>
    ...     <li>2</li>
    ...     <li class="selected">3</li>
    ...     <li>4</li>
    ...     <li>5</li>
    ... </ul>"""
    >>> WebDriver().open(snippet).find('li.selected').prev
    WebElementSet(
      <li>2</li>
    )

next_all
--------

Get all following siblings of each element in the set of matched elements,
optionally filtered by a selector.

.. code-block:: python

    >>> from webdriverplus import WebDriver
    >>> snippet = """
    ... <ul>
    ...     <li>1</li>
    ...     <li>2</li>
    ...     <li class="selected">3</li>
    ...     <li>4</li>
    ...     <li>5</li>
    ... </ul>"""
    >>> WebDriver().open(snippet).find('li.selected').next_all
    WebElementSet(
      <li>4</li>
      <li>5</li>
    )

prev_all
--------

Get all preceding siblings of each element in the set of matched elements,
optionally filtered by a selector.

.. code-block:: python

    >>> from webdriverplus import WebDriver
    >>> snippet = """
    ... <ul>
    ...     <li>1</li>
    ...     <li>2</li>
    ...     <li class="selected">3</li>
    ...     <li>4</li>
    ...     <li>5</li>
    ... </ul>"""
    >>> WebDriver().open(snippet).find('li.selected').prev_all
    WebElementSet(
      <li>1</li>
      <li>2</li>
    )

siblings
--------

Get the siblings of each element in the set of matched elements, optionally
filtered by a selector.

.. code-block:: python

    >>> from webdriverplus import WebDriver
    >>> snippet = """
    ... <ul>
    ...     <li>1</li>
    ...     <li>2</li>
    ...     <li class="selected">3</li>
    ...     <li>4</li>
    ...     <li>5</li>
    ... </ul>"""
    >>> WebDriver().open(snippet).find('li.selected').siblings
    WebElementSet(
      <li>1</li>
      <li>2</li>
      <li>4</li>
      <li>5</li>
    )
