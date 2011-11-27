.. _inspection:

Inspection & Manipulation
=========================

.style
------

Returns an object that lets you get and set the CSS style of an element.

.. code-block:: python

    >>> import webdriverplus
    >>> driver = webdriverplus.Firefox()
    >>> driver.get('http://www.google.com')
    >>> driver.find_all('input').style.background = 'green'
    >>> driver.find('body').style.background = 'red'

.size
-----

Returns the size of the element, as a ``namedtuple``.

    >>> elem.size
    Size(width=300, height=25)
    >>> width, height = elem.size
    >>> width = elem.size.width

.location
---------

Returns the location of the element in the canvas, as a ``namedtuple``.

    >>> elem.location
    Location(x=10, y=50)
    >>> x, y = elem.location
    >>> x = elem.location.x
    >>> y = elem.location.y

.value
------

.is_checked
-----------

.is_selected
------------

.is_enabled
-----------

.is_visible
-----------

.class
------

Returns the set of CSS classes applied on the element.

.id
---

Returns the 'id' attribute of the element.

.tag_name
---------

Returns the element's tag name.  (Eg. 'h1', 'div', 'input')

.attributes
-----------

Returns a dictionary-like object representing all the DOM attributes on the
element.  Supports getting, setting, and deleting attributes.

    >>> elem = driver.find(id='logo')
    >>> elem.attributes
    {u'width': u'50px', u'src': u'/static/images/logo.png', u'height': u'50px'}
    >>> elem.attributes['src']
    u'/static/images/logo.png'
    >>> elem.attribtues['src'] = '/static/images/other.png'
    >>> del(elem.attributes['width'])
    >>> del(elem.attributes['height'])
    >>> elem.attributes
    {u'src': u'/static/images/other.png'}

.. note::

    The values returned by ``.attributes`` differ slightly from those
    returned by WebDriver's ``.get_attribute()``.

    Eg: When dealing with sizes, ``.attribute['height']`` returns a value like
    ``50px`` where ``.getAttribute('height')`` returns a value like ``50``.
    When dealing with links, ``.attribute['src']`` returns the raw src value,
    where ``.getAttribute('src')`` returns an absolute URL.

    Both styles are supported by WebDriver Plus.
