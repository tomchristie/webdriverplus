.. _actions:

Actions
=======

Actions in WebDriver Plus always operate on the first element in the
``WebElementSet``.  If you want to apply an action to each element in the
set, you should iterate over the set:

.. code-block:: python

    for elem in browser.find('input', type='checkbox'):
        elem.check()

Actions return the original ``WebElementSet``, which means they can be chained.
For example:

.. code-block:: python

    elem = browser.find(id='username')
    elem.send_keys('denvercoder9').submit()

Supported actions
~~~~~~~~~~~~~~~~~

Currently the following actions are supported.

.. note::
    Many actions are not yet fully supported natively through WebDriver, and have
    to instead be simulated using javascript.  As a result it's possible that some
    behavior may vary slightly between different web browsers.

.click()
--------

Clicks an element.

.double_click()
---------------

Double-clicks an element.

.context_click()
----------------

Performs a context-click (right click) on an element.

.move_to()
----------

Moves the mouse to center over an element.

.click_and_hold()
-----------------

Holds down on an element.

.release()
----------

Releases a held click.

.check()
----------

Clicks a checkbox if it isn't already checked.

.uncheck()
----------

Clicks a checkbox to uncheck it if it's checked.

.submit()
---------

If the element is a form, submit it.  Otherwise search for a form enclosing
the element, and submit that.

.clear()
--------

Clears any user editable text from the element.

.send_keys(*text*)
------------------

Sends keys to an element.
