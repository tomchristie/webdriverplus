.. _selectors:

Selectors
=========

.. code-block:: python

    import webdriverplus
    driver = webdriverplus.Firefox()
    driver.get('http://www.example.com/')
    driver.find(id='loginform')
    driver.find(css='ul li.selected')
    driver.find(name='username')
    driver.find(tag_name='h1')
    driver.find(class_name='selected')
    driver.find(xpath='//ul/li[@class="selected"]')
    driver.find(text='Welcome to my site')
    driver.find(text_contains=('Welcome'))
    driver.find(attribute='checked')
    driver.find(attribute_value=('checked', 'true'))
    driver.find(value='foobar')
    driver.find(type='checkbox')
    driver.find('input', type='checkbox', checked=True)
    driver.find('option', selected=False)

id
--

css
---

name
----

tag_name
--------

class_name
----------

xpath
-----

text
----

text_contains
-------------

attribute
---------

attribute_value
---------------

