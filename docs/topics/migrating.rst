.. _migrating:

Migrating to WebDriver Plus
---------------------------

Where possible WebDriver Plus remains compatible with WebDriver, which means
that migrating can often be as simple as importing ``webdriverplus`` in place
of ``webdriver``:

.. code-block:: python

    import webdriverplus as webdriver

.. todo::

    List incompatible changes.
    Explain relation between base classes in each.

.. note::

    If you're migrating from ``webdriver`` to ``webdriverplus``, please
    consider making a note of any issues you come across, and letting me know.
