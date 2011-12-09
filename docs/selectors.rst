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

id = *<string>*
---------------

css = *<string>*
----------------

name = *<string>*
-----------------

tag_name = *<string>*
---------------------

class_name = *<string>*
-----------------------

xpath = *<string>*
------------------

text = *<string>*
-----------------

text_contains = *<string>*
--------------------------

link_text = *<string>*
----------------------

link_text_contains = *<string>*
-------------------------------

label_text = *<string>*
-----------------------

label_text_contains = *<string>*
--------------------------------

attribute = *<string>*
----------------------

attribute_value = *<tuple of (string, string)>*
-----------------------------------------------

value = *<string>*
------------------

type = *<string>*
-----------------

checked = *<bool>*
------------------

selected = *<bool>*
-------------------
