.. _forms:

Form Submission
===============

.. code-block:: python

    form = driver.get_form(id='login')
    form.username = 'tomchristie'
    form.password = 'foobar9'
    form.remember_me = False
    form.submit()
