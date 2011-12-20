.. _traversing:

Traversing
==========

children
--------

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

ancestors
---------

.. code-block:: python

    >>> from webdriverplus import WebDriver
    >>> snippet = """
    ... <ul>
    ...     <li>1</li>
    ...     <li class="selected">2</li>
    ...     <li>3</li>
    ... </ul>"""
    >>> WebDriver().open(snippet).find('.selected').ancestors
    WebElementSet(
      <html webdriver="true"><head></head><body><ul> <li>1</li> <li class="select...
      <body><ul> <li>1</li> <li class="selected">2</li> <li>3</li> </ul></body>
      <ul> <li>1</li> <li class="selected">2</li> <li>3</li> </ul>
    )

next
----

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
