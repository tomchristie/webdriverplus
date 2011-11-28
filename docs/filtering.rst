.. _filtering:

Filtering
=========

.filter(*selector*)
-------------------

Filters the ``WebElementSet`` to only include elements that match the selector.

.. code-block:: python

    >>> import webdriverplus
    >>> driver = webdriverplus.Firefox()
    >>> snippet = """
    ... <ul>
    ...     <li>1</li>
    ...     <li class="selected">2</li>
    ...     <li>3</li>
    ...     <li>4</li>
    ...     <li class="selected">5</li>
    ... </ul>"""
    >>> driver.open(snippet).find('li').filter(class_name='selected').html
    ['<li class="selected">2</li>', '<li class="selected">5</li>']


.exclude(*selector*)
--------------------

Filters the ``WebElementSet`` to only include elements that do not match the
selector.

.. code-block:: python

    >>> import webdriverplus
    >>> driver = webdriverplus.Firefox()
    >>> snippet = """
    ... <ul>
    ...     <li>1</li>
    ...     <li class="selected">2</li>
    ...     <li>3</li>
    ...     <li>4</li>
    ...     <li class="selected">5</li>
    ... </ul>"""
    >>> driver.open(snippet).find('li').exclude(class_name='selected').html
    ['<li>1</li>', '<li>3</li>', '<li>4</li>']

.closest(*selector*)
--------------------

