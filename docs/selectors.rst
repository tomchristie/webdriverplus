.. _selectors:

Selectors
=========

Finding elements on the page
----------------------------

WebDriver Plus supports a wide variety of selectors to let you easily locate
elements on the page.

To locate elements on the page use the ``.find()`` method.  Calling
``.find()`` will return a set of all the elements that matched the selectors.

.. code-block:: python

    import webdriverplus
    browser = webdriverplus.WebDriver()
    browser.get('http://www.example.com/')
    browser.find(id='login-form')

Different types of selector are used depending on the keyword arguments
passed to ``find()``.

.. code-block:: python

    browser.find(id='login-form')
    browser.find(tag_name='a')
    browser.find(css='#login-form input')
    browser.find(link_text='Images')

The default selector for the ``.find()`` method is ``css``.  If you pass an
unnamed argument to ``.find()`` it will be treated as a css selector.

.. code-block:: python

    browser.find('a')              # All 'a' tags
    browser.find('a.selected')     # All 'a' tags with 'selected' class
    browser.find('div#content a')  # All 'a' tags within the 'content' div

Multiple selectors can be used in a single expression.  The resulting set will
be the set of elements that match all the given selectors.  **TODO**

.. code-block:: python

    browser.find('input', type='checkbox', checked=True)

.. note::

    When finding elements and traversing the DOM, WebDriver Plus follows the
    same style as JQuery.

    You will always be working with sets of WebElements rather than indivdual
    elements.  Actions on those sets, such as ``.click()``, will applied only
    to the first element in the set.

Chaining selectors
------------------

The ``.find()`` method can be applied either to the browser instance, or to an
existing set of elements.  When applied to an existing set of elements
``.find()`` will return all children of any element in the set that match the
given selector.

.. code-block:: python

    login = browser.find(id='login-form')  # The login form
    inputs = login.find('input')           # All 'input' tags within the form

Selectors can also be chained in a single expression.

.. code-block:: python

    browser.find(id='login-form').find('input')

Supported selectors
-------------------

css
~~~

id
~~

name
~~~~

tag_name
~~~~~~~~

class_name
~~~~~~~~~~

xpath
~~~~~

text
~~~~

text_contains
~~~~~~~~~~~~~

link_text
~~~~~~~~~

link_text_contains
~~~~~~~~~~~~~~~~~~

attribute
~~~~~~~~~

attribute_value
~~~~~~~~~~~~~~~

value
~~~~~

type
~~~~

checked
~~~~~~~

selected
~~~~~~~~
