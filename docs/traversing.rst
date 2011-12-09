.. _traversing:

Traversing
==========

children
--------

.. code-block:: python

    >>> import webdriverplus
    >>> driver = webdriverplus.Firefox()
    >>> snippet = """<html>
    ...     <ul>
    ...         <li>1</li>
    ...         <li><strong>2</strong></li>
    ...         <li>3</li>
    ...     </ul>
    ... </html>"""
    >>> driver.open(snippet).find('ul').children.html
    ['<li>1</li>', '<li><strong>2</strong></li>', '<li>3</li>']


parent
------

.. code-block:: python

    >>> import webdriverplus
    >>> driver = webdriverplus.Firefox()
    >>> snippet = """<html>
    ...     <ul>
    ...         <li>1</li>
    ...         <li><strong>2</strong></li>
    ...         <li>3</li>
    ...     </ul>
    ... </html>"""
    >>> driver.open(snippet).find('strong').parent
    '<li><strong>2</strong></li>'

descendants
-----------

.. code-block:: python

    >>> import webdriverplus
    >>> driver = webdriverplus.Firefox()
    >>> snippet = """<html>
    ...     <ul>
    ...         <li>1</li>
    ...         <li><strong>2</strong></li>
    ...         <li>3</li>
    ...     </ul>
    ... </html>"""
    >>> driver.open(snippet).find('ul').descendants
    ['<li>1</li>', '<li><strong>2</strong></li>', '<strong>2</strong>', '<li>3</li>']

ancestors
---------

.. code-block:: python

    >>> import webdriverplus
    >>> driver = webdriverplus.Firefox()
    >>> snippet = """<html>
    ...     <ul>
    ...         <li>1</li>
    ...         <li class="selected">2</li>
    ...         <li>3</li>
    ...     </ul>
    ... </html>"""
    >>> driver.open(snippet).find('.selected').ancestors
    WebElementSet(<html>, <body>, <ul>)

next
----

.. code-block:: python

    >>> import webdriverplus
    >>> driver = webdriverplus.Firefox()
    >>> snippet = """<html>
    ...     <ul>
    ...         <li>1</li>
    ...         <li>2</li>
    ...         <li class="selected">3</li>
    ...         <li>4</li>
    ...         <li>5</li>
    ...     </ul>
    ... </html>"""
    >>> driver.open(snippet).find('li.selected').next
    ['<li>4</li>']

prev
----

.. code-block:: python

    >>> import webdriverplus
    >>> driver = webdriverplus.Firefox()
    >>> snippet = """<html>
    ...     <ul>
    ...         <li>1</li>
    ...         <li>2</li>
    ...         <li class="selected">3</li>
    ...         <li>4</li>
    ...         <li>5</li>
    ...     </ul>
    ... </html>"""
    >>> driver.open(snippet).find('li.selected').prev
    ['<li>2</li>']

next_all
--------

.. code-block:: python

    >>> import webdriverplus
    >>> driver = webdriverplus.Firefox()
    >>> snippet = """<html>
    ...     <ul>
    ...         <li>1</li>
    ...         <li>2</li>
    ...         <li class="selected">3</li>
    ...         <li>4</li>
    ...         <li>5</li>
    ...     </ul>
    ... </html>"""
    >>> driver.open(snippet).find('li.selected').next_all
    ['<li>4</li>', '<li>5</li>']

prev_all
--------

.. code-block:: python

    >>> import webdriverplus
    >>> driver = webdriverplus.Firefox()
    >>> snippet = """<html>
    ...     <ul>
    ...         <li>1</li>
    ...         <li>2</li>
    ...         <li class="selected">3</li>
    ...         <li>4</li>
    ...         <li>5</li>
    ...     </ul>
    ... </html>"""
    >>> driver.open(snippet).find('li.selected').prev_all
    ['<li>1</li>', '<li>2</li>']

siblings
--------

.. code-block:: python

    >>> import webdriverplus
    >>> driver = webdriverplus.Firefox()
    >>> snippet = """<html>
    ...     <ul>
    ...         <li>1</li>
    ...         <li>2</li>
    ...         <li class="selected">3</li>
    ...         <li>4</li>
    ...         <li>5</li>
    ...     </ul>
    ... </html>"""
    >>> driver.open(snippet).find('li.selected').siblings
    ['<li>1</li>', '<li>2</li>', '<li>4</li>', '<li>5</li>']
