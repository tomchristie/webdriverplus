#!/usr/bin/env python
# coding: utf-8

import sys
import unittest
import warnings

import webdriverplus
from selenium.webdriver.common.keys import Keys

# WebElements as set

# close_on_shutdown
# default_selector
# base_url

# drag & drop

# find_all().find() is broken
# No such element exceptions need to be cleaner

run_slow_tests = '--all' in sys.argv
browser = 'firefox'

# Support unicode literals for all versions
if sys.version < '3':
    import codecs

    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x


class WebDriverPlusTests(unittest.TestCase):
    extra_webdriver_kwargs = {}

    def setUp(self):
        self.driver = webdriverplus.WebDriver(browser, reuse_browser=True,
                                              **self.extra_webdriver_kwargs)

    def tearDown(self):
        self.driver.quit()


if run_slow_tests:
    class BrowserPoolingTests(unittest.TestCase):
        # Note: We don't inherit from WebDriverPlusTests as we don't want the
        #       default reuse browser behaviour for theses tests.

        # TODO: Similar tests, but with multiple windows open.

        def setUp(self):
            webdriverplus.WebDriver._pool.pop('firefox', None)

        def tearDown(self):
            for browser, signature in webdriverplus.WebDriver._pool.values():
                browser.quit(force=True)

        def test_reuse_browser_set(self):
            browser = webdriverplus.WebDriver('firefox', reuse_browser=True)
            browser.quit()
            other = webdriverplus.WebDriver('firefox', reuse_browser=True)
            self.assertEqual(browser, other)

        def test_reuse_browser_unset(self):
            browser = webdriverplus.WebDriver('firefox')
            browser.quit()
            other = webdriverplus.WebDriver('firefox')
            self.assertNotEqual(browser, other)


class DriverTests(WebDriverPlusTests):
    def test_open(self):
        page_text = 'abc'
        self.driver.open(page_text)
        self.assertEqual(self.driver.page_text,  page_text)

    def test_find(self):
        self.driver.open(u('<h1>123</h1><h2>☃</h2><h3>789</h3>'))
        self.assertEqual(self.driver.find('h2').text, u('☃'))

    def test_find_wait(self):
        self.driver.open('<h1 id="t">123</h1>')
        js = """
        setTimeout(
          function () {
            // create a new div element
            // and give it some content
            var newDiv = document.createElement("div");
            var newContent = document.createTextNode("Hello");

            newDiv.appendChild(newContent); //add the text node to the newly created div.

            // add the newly created element and it's content into the DOM
            h1 = document.getElementById("t");
            document.body.insertBefore(newDiv, h1);
          },
          1000
          )
        """
        self.driver.execute_script(js)
        self.assertEqual(self.driver.find('div', wait=2).text, 'Hello')

    def test_unicode(self):
        self.driver.open('<h1>123</h1><h2>456</h2><h3>789</h3>')
        self.assertEqual(self.driver.find('h2').text, '456')

    def test_iframe(self):
        self.driver.open('<p>Test iframe</p><iframe></iframe>')
        self.assertEqual(self.driver.find('p').text, 'Test iframe')
        self.driver.switch_to_frame(self.driver.find('iframe'))
        self.assertFalse(self.driver.find('p'))

    def test_wait_for(self):
        self.driver.open('<h1 id="t" style="display:none">123</h1>')
        self.assertFalse(self.driver.find('#t').is_displayed())
        self.driver.execute_script(
            'setTimeout(function () { document.getElementById("t").style.display="block"}, 1000)')
        self.driver.wait_for('#t', wait=2)
        self.assertTrue(self.driver.find('#t').is_displayed())

    def test_wait_for2(self):
        self.driver.open('<h1 id="t" style="display:none">123</h1>')
        self.assertFalse(self.driver.find('#t').is_displayed())
        self.driver.execute_script(
            'setTimeout(function () { document.getElementById("t").style.display="block"}, 1000)')
        self.driver.wait_for(text='123', wait=2)
        el = self.driver.find(text='123')
        self.assertTrue(el.is_displayed())
        self.assertEqual(el.text, '123')

    def test_wait_for3(self):
        self.driver.open('<h1 id="t" style="display:none">123</h1>')
        self.assertFalse(self.driver.find('#t').is_displayed())
        self.driver.execute_script(
            'setTimeout(function () { document.getElementById("t").style.display="block"}, 1000)')

        self.driver.wait_for('h1', text='123', wait=2)
        el = self.driver.find('h1', text='123', wait=2)
        self.assertTrue(el.is_displayed())
        self.assertEqual(el.text, '123')


class SelectorTests(WebDriverPlusTests):
    def setUp(self):
        super(SelectorTests, self).setUp()
        snippet = """<html>
                         <h1>header</h1>
                         <ul id="mylist">
                             <li>one</li>
                             <li>two</li>
                             <li class="selected">three</li>
                             <li><a href="#">four</a></li>
                             <li><strong>hi</strong>five</li>
                             <li>six<strong>hi</strong></li>
                             <li><strong>seven</strong></li>
                             <span>one</span>
                         </ul>
                         <form>
                             <label for="username">Username:</label>
                             <input type="text" name="username" value="lucy"/>
                             <label for="password">Password:</label>
                             <input type="password" name="password" />
                             <select>
                                <option value='1'>1</option>
                                <option value='2'>2</option>
                             </select>
                         </form>
                         <form id="checkboxlist">
                             <input type="checkbox" value="red" />
                             <input type="checkbox" value="green" />
                             <input type="checkbox" value="blue" checked=yes />
                         </form>
                     </html>"""
        self.driver.open(snippet)

    def test_multiple_selectors(self):
        node = self.driver.find('li', text='one')
        self.assertEqual(node.html, '<li>one</li>')

    def test_nonexistant_multiple_selectors(self):
        """If a combination of selector doesn't match one or more
        elements, none should be returned."""
        nodes = self.driver.find('li', text='fubar')
        self.assertFalse(nodes)

    def test_multiple_named_selectors(self):
        node = self.driver.find(tag_name='li', text='one')
        self.assertEqual(node.html, '<li>one</li>')

    def test_nonexistant_multiple_named_selectors(self):
        """If a combination of named selector doesn't match one or more
        elements, none should be returned."""
        nodes = self.driver.find(tag_name='li', text='fubar')
        self.assertFalse(nodes)

    def test_id(self):
        node = self.driver.find(id='mylist')
        self.assertEqual(node.tag_name, 'ul')

    def test_class_name(self):
        node = self.driver.find(class_name='selected')
        self.assertEqual(node.text, 'three')

    def test_tag_name(self):
        node = self.driver.find(tag_name='h1')
        self.assertEqual(node.text, 'header')

    def test_name(self):
        node = self.driver.find(name='username')
        self.assertEqual(node.tag_name, 'input')
        self.assertEqual(node.value, 'lucy')

    def test_css(self):
        node = self.driver.find(css='ul li.selected')
        self.assertEqual(node.text, 'three')

    def test_xpath(self):
        node = self.driver.find(xpath='//ul/li[@class="selected"]')
        self.assertEqual(node.text, 'three')

    def test_link_text(self):
        node = self.driver.find(link_text='four')
        self.assertEqual(node.tag_name, 'a')
        self.assertEqual(node.text, 'four')

    def test_link_text_contains(self):
        node = self.driver.find(link_text_contains='ou')
        self.assertEqual(node.tag_name, 'a')
        self.assertEqual(node.text, 'four')

    def test_text(self):
        self.assertEqual(self.driver.find(text='one').index, 0)
        self.assertEqual(self.driver.find(text='two').index, 1)
        self.assertEqual(self.driver.find(text='three').index, 2)

    def test_text_contains(self):
        self.assertEqual(self.driver.find('li', text_contains='ne').index, 0)
        self.assertEqual(self.driver.find('li', text_contains='tw').index, 1)
        self.assertEqual(self.driver.find('li', text_contains='hre').index, 2)

        self.assertEqual(len(self.driver.find(text_contains='ne')), 2)
        self.assertEqual(len(self.driver.find(text_contains='tw')), 1)
        self.assertEqual(len(self.driver.find(text_contains='hre')), 1)

        self.assertEqual(len(self.driver.find('li', text_contains='ive')), 1)
        self.assertEqual(len(self.driver.find('li', text_contains='ix')), 1)
        self.assertEqual(len(self.driver.find('li', text_contains='eve')), 0)

    #def test_label(self):
    #    node = self.driver.find(label='Password:')
    #    expected = '<input type="password" name="password" />'
    #    self.assertEqual(node.html, expected)

    #def test_label_contains(self):
    #    node = self.driver.find(label_contains='Password')
    #    expected = '<input type="password" name="password" />'
    #    self.assertEqual(node.html, expected)

    def test_attribute(self):
        node = self.driver.find(attribute='checked')
        self.assertEqual(node.value, 'blue')

    def test_attribute_value(self):
        node = self.driver.find(attribute_value=('checked', 'yes'))
        self.assertEqual(node.value, 'blue')

    def test_value(self):
        node = self.driver.find(value='blue')
        self.assertEqual(node.tag_name, 'input')
        self.assertEqual(node.type, 'checkbox')
        self.assertEqual(node.value, 'blue')

    def test_value_setter(self):
        node = self.driver.find('input[type="text"]')
        self.assertEqual(node.value, 'lucy')
        node.value = 'lucyyy'
        node = self.driver.find('input[type="text"]')
        self.assertEqual(node.value, 'lucyyy')

    def test_value_setter_select(self):
        node = self.driver.find('select')
        node.value = '2'
        node = self.driver.find('select')
        self.assertEqual(node.value, '2')

    def test_type(self):
        node = self.driver.find(type='checkbox')
        self.assertEqual(node.value, 'red')

    def test_checked(self):
        elem = self.driver.find(id='checkboxlist')
        self.assertEqual(len(elem.find(checked=True)), 1)
        self.assertEqual(len(elem.find(checked=False)), 2)

        # TODO: checked=True, checked=False, selected=True, selected=False


class TraversalTests(WebDriverPlusTests):
    def setUp(self):
        super(TraversalTests, self).setUp()
        snippet = """<html>
                         <ul>
                             <li>1</li>
                             <li>2</li>
                             <li class="selected">3</li>
                             <li>4</li>
                             <li><strong>5</strong></li>
                         </ul>
                     </html>"""
        self.driver.open(snippet)

    def test_indexing(self):
        elem = self.driver.find('ul').children()[0]
        self.assertEqual(elem.html, '<li>1</li>')

    def test_slicing(self):
        elems = self.driver.find('ul').children()[0:-1]
        expected = [
            '<li>1</li>',
            '<li>2</li>',
            '<li class="selected">3</li>',
            '<li>4</li>'
        ]
        self.assertEqual([elem.html for elem in elems], expected)

    def test_children(self):
        nodes = self.driver.find('ul').children()
        text = [node.text for node in nodes]
        self.assertEqual(text, ['1', '2', '3', '4', '5'])

    def test_filtering_traversal(self):
        nodes = self.driver.find('ul').children('.selected')
        text = [node.text for node in nodes]
        self.assertEqual(text, ['3'])

    def test_parent(self):
        node = self.driver.find('.selected').parent()
        self.assertEqual(node.tag_name, 'ul')

    def test_descendants(self):
        nodes = self.driver.find('ul').descendants()
        tag_names = [node.tag_name for node in nodes]
        self.assertEqual(tag_names, ['li', 'li', 'li', 'li', 'li', 'strong'])

    def test_ancestors(self):
        nodes = self.driver.find(class_name='selected').ancestors()
        tag_names = [node.tag_name for node in nodes]
        self.assertEqual(tag_names, ['html', 'body', 'ul'])

    def test_next(self):
        node = self.driver.find('.selected').next()
        self.assertEqual(node.text, '4')

    def test_prev(self):
        node = self.driver.find('.selected').prev()
        self.assertEqual(node.text, '2')

    def test_next_all(self):
        nodes = self.driver.find('.selected').next_all()
        text = [node.text for node in nodes]
        self.assertEqual(text, ['4', '5'])

    def test_prev_all(self):
        nodes = self.driver.find('.selected').prev_all()
        text = [node.text for node in nodes]
        self.assertEqual(text, ['1', '2'])

    def test_siblings(self):
        nodes = self.driver.find('.selected').siblings()
        text = [node.text for node in nodes]
        self.assertEqual(text, ['1', '2', '4', '5'])


class FilteringTests(WebDriverPlusTests):
    def setUp(self):
        super(FilteringTests, self).setUp()
        snippet = """<ul>
                         <li>1</li>
                         <li>2</li>
                         <li class="selected">3</li>
                         <li>4</li>
                         <li class="selected">5</li>
                     </ul>"""
        self.driver.open(snippet)

    def test_filter(self):
        nodes = self.driver.find('li').filter('.selected')
        self.assertEqual([node.text for node in nodes], ['3', '5'])

    def test_exclude(self):
        nodes = self.driver.find('li').exclude('.selected')
        self.assertEqual([node.text for node in nodes], ['1', '2', '4'])


class ShortcutTests(WebDriverPlusTests):
    def setUp(self):
        super(ShortcutTests, self).setUp()
        snippet = """<ul id='list'>
                         <li>1</li>
                         <li>2</li>
                         <li class="selected">3</li>
                         <li>4</li>
                         <li>5</li>
                     </ul>"""
        self.driver.open(snippet)

    def test_index(self):
        node = self.driver.find('.selected')
        self.assertEqual(node.index, 2)

    def test_html(self):
        node = self.driver.find('.selected')
        self.assertEqual(node.html, '<li class="selected">3</li>')

    def test_inner_html(self):
        node = self.driver.find('.selected')
        self.assertEqual(node.inner_html, '3')

    def test_has_class(self):
        node = self.driver.find(css='ul li.selected')
        self.assertTrue(node.has_class('selected'))

    def test_set_has_class(self):
        nodes = self.driver.find(css='ul li')
        self.assertTrue(nodes.has_class('selected'))

    def test_attr(self):
        node = self.driver.find(css='ul li.selected')
        self.assertEqual(node.attr('class'), 'selected')

    def test_attr_id(self):
        node = self.driver.find('ul')
        self.assertEqual(node.attr('id'), 'list')


class InspectionTests(WebDriverPlusTests):
    def setUp(self):
        super(InspectionTests, self).setUp()
        snippet = """<html>
                         <head>
                             <style type="text/css">
                                 .selected {color: red}
                                 img {width: 100px; height: 50px;}
                             </style>
                         </head>
                         <body>
                             <img src='#' width='100px' height='50px'>
                             <ul style="color: blue">
                                 <li>1</li>
                                 <li>2</li>
                                 <li class="selected">3</li>
                                 <li>4</li>
                                 <li>5</li>
                             </ul>
                         </body>
                     </html>"""
        self.driver.open(snippet)

    def test_get_style_inline(self):
        elem = self.driver.find('ul')
        self.assertTrue(elem.css('color') in ('#0000ff', 'blue', 'rgb(0, 0, 255)', 'rgba(0, 0, 255, 1)'))

    def test_get_style_css(self):
        elem = self.driver.find('.selected')
        self.assertTrue(elem.css('color'), ('#ff0000', 'red', 'rgb(255, 0, 0)', 'rgba(255 ,0, 0, 1)'))

    def test_set_style(self):
        elem = self.driver.find('.selected')
        elem.css('color', 'green')
        self.assertTrue(elem.css('color') in ('#008000', 'green', 'rgb(0, 128, 0)', 'rgba(0, 128, 0, 1)'))

    def test_set_style2(self):
        elem = self.driver.find('.selected')
        elem.css('color', 'blue')
        self.assertTrue(elem.css('color') in ('#0000ff', 'blue', 'rgb(0, 0, 255)', 'rgba(0, 0, 255, 1)'))
        # Test for setting css style with dash
        elem.css('background-color', 'blue')
        self.assertTrue(elem.css('background-color') in ('#0000ff', 'blue', 'rgb(0, 0, 255)', 'rgba(0, 0, 255, 1)'))
        elem.css('backgroundColor', 'green')
        self.assertTrue(elem.css('backgroundColor') in ('#008000', 'green', 'rgb(0, 128, 0)', 'rgba(0, 128, 0, 1)'))

    def test_size(self):
        elem = self.driver.find('img')
        self.assertEqual(elem.size.width, 100)
        self.assertEqual(elem.css('width'), '100px')
        self.assertEqual(elem.size.height, 50)
        self.assertEqual(elem.css('height'), '50px')

    def test_size_unpacked(self):
        (width, height) = self.driver.find('img').size
        self.assertEqual(width, 100)
        self.assertEqual(height, 50)

    def test_attributes(self):
        elem = self.driver.find('img')
        self.assertEqual(elem.attributes,
                          {'width': '100px', 'height': '50px', 'src': '#'})
        self.assertEqual(set(elem.attributes.keys()),
                          set(['width', 'height', 'src']))
        self.assertEqual(set(elem.attributes.values()),
                          set(['100px', '50px', '#']))

    def test_get_attribute(self):
        elem = self.driver.find('img')
        self.assertEqual(elem.attributes['width'], '100px')

    def test_set_attribute(self):
        elem = self.driver.find('img')
        elem.attributes['width'] = '33px'
        self.assertEqual(elem.attributes['width'], '33px')

    def test_del_attribute(self):
        elem = self.driver.find('img')
        del elem.attributes['src']
        self.assertEqual(elem.attributes,
                          {'width': '100px', 'height': '50px'})


class FormInspectionTests(WebDriverPlusTests):
    def setUp(self):
        super(FormInspectionTests, self).setUp()
        snippet = """<html>
                         <form>
                             <select multiple>
                                 <option selected>Walk</option>
                                 <option>Cycle</option>
                                 <option>Drive</option>
                             </select>
                             <fieldset>
                                 <input type="checkbox" value="peanuts" />
                                 I like peanuts
                             </fieldset>
                             <fieldset>
                                 <input type="checkbox" value="jam" checked />
                                 I like jam
                             </fieldset>
                         </form>
                     </html>"""
        self.driver.open(snippet)

    def test_is_selected(self):
        elem = self.driver.find('form')
        self.assertTrue(elem.find(text='Walk').is_selected())
        self.assertFalse(elem.find(text='Cycle').is_selected())
        self.assertFalse(elem.find(text='Drive').is_selected())

    def test_is_checked(self):
        elem = self.driver.find('form')
        self.assertFalse(elem.find(value='peanuts').is_checked())
        self.assertTrue(elem.find(value='jam').is_checked())

    def test_deselect_option(self):
        elem = self.driver.find('form select')
        elem.deselect_option(text='Walk')
        self.assertFalse(elem.attr('value'))
        self.assertFalse(elem.find(text='Walk').is_selected())

    def test_select_option(self):
        elem = self.driver.find('form select')
        elem.select_option(text='Cycle')
        self.assertTrue(elem.find(text='Cycle').is_selected())


class ValueTests(WebDriverPlusTests):
    def setUp(self):
        super(ValueTests, self).setUp()
        snippet = """<form>
                         <input type="text" name="username" value="mike">
                     </form>"""
        self.driver.open(snippet)

    def test_get_value(self):
        pass

    def test_set_value(self):
        pass


class InputTests(WebDriverPlusTests):
    def setUp(self):
        super(InputTests, self).setUp()
        snippet = """<form>
                         <input type="text" name="username" value="mike">
                     </form>"""
        self.driver.open(snippet)

    def test_send_keys(self):
        elem = self.driver.find('input')
        elem.send_keys("hello")

    def test_type_keys(self):
        elem = self.driver.find('input')
        elem.type_keys("hello")


class SetTests(WebDriverPlusTests):
    def setUp(self):
        super(SetTests, self).setUp()
        snippet = """<ul>
                         <li>1</li>
                         <li>2</li>
                         <li>3</li>
                         <li>4</li>
                         <li>5</li>
                     </ul>
                     <ul>
                         <li>a</li>
                         <li>b</li>
                         <li>c</li>
                     </ul>"""
        self.driver.open(snippet)

    def test_set_uniqueness(self):
        nodes = self.driver.find('li')
        self.assertEqual(len(nodes), 8)
        self.assertEqual(len(nodes.parent()), 2)


class ActionTests(WebDriverPlusTests):
    # TODO: Urg.  Refactor these
    def test_click(self):
        js = "document.getElementById('msg').innerHTML = 'click'"
        snippet = "<div id='msg'></div><a onclick=\"%s\">here</a>" % js
        self.driver.open(snippet).find('a').click()
        self.assertEqual(self.driver.find(id='msg').text, 'click')

    def test_double_click(self):
        js = "document.getElementById('msg').innerHTML = 'double click'"
        snippet = "<div id='msg'></div><a onDblclick=\"%s\">here</a>" % js
        self.driver.open(snippet).find('a').double_click()
        self.assertEqual(self.driver.find(id='msg').text, 'double click')

    def test_context_click(self):
        js = "document.getElementById('msg').innerHTML = event.button;"
        snippet = "<div id='msg'></div><a oncontextmenu=\"%s\">here</a>" % js
        self.driver.open(snippet).find('a').context_click()
        self.assertEqual(self.driver.find(id='msg').text, '2')

        # context menu stays open, so close it
        self.driver.find('body').send_keys(Keys.ESCAPE)

    def test_click_and_hold(self):
        js = "document.getElementById('msg').innerHTML = 'mouse down'"
        snippet = "<div id='msg'></div><a onMouseDown=\"%s\">here</a>" % js
        self.driver.open(snippet).find('a').click_and_hold()
        self.assertEqual(self.driver.find(id='msg').text, 'mouse down')

    def test_release(self):
        js = "document.getElementById('msg').innerHTML = 'mouse up'"
        snippet = "<div id='msg'></div><a onMouseUp=\"%s\">here</a>" % js
        elem = self.driver.open(snippet).find('a')
        elem.click_and_hold()
        self.assertEqual(self.driver.find(id='msg').text, '')
        elem.release()
        self.assertEqual(self.driver.find(id='msg').text, 'mouse up')

    def test_move_to(self):
        js = "document.getElementById('msg').innerHTML = 'mouse over'"
        snippet = "<div id='msg'></div><a onMouseOver=\"%s\">here</a>" % js
        self.driver.open(snippet).find('a').move_to()
        self.assertEqual(self.driver.find(id='msg').text, 'mouse over')

    def test_move_to_and_click(self):
        js = "document.getElementById('msg').innerHTML = 'click'"
        snippet = "<div id='msg'></div><a onClick=\"%s\">here</a>" % js
        self.driver.open(snippet).find('a').move_to_and_click()
        self.assertEqual(self.driver.find(id='msg').text, 'click')

    def test_check_unchecked(self):
        snippet = "<form><input type='checkbox' id='cbx'> Checkbox</form>"
        self.driver.open(snippet).find('#cbx').check()
        self.assertEqual(self.driver.find('#cbx').get_attribute('checked'), 'true')

    def test_check_checked(self):
        snippet = "<form><input type='checkbox' id='cbx' checked='checked'> Checkbox</form>"
        self.driver.open(snippet).find('#cbx').check()
        self.assertEqual(self.driver.find('#cbx').get_attribute('checked'), 'true')

    def test_uncheck_unchecked(self):
        snippet = "<form><input type='checkbox' id='cbx'> Checkbox</form>"
        self.driver.open(snippet).find('#cbx').uncheck()
        self.assertEqual(self.driver.find('#cbx').get_attribute('checked'), None)

    def test_uncheck_checked(self):
        snippet = "<form><input type='checkbox' id='cbx' checked='checked'> Checkbox</form>"
        self.driver.open(snippet).find('#cbx').uncheck()
        self.assertEqual(self.driver.find('#cbx').get_attribute('checked'), None)

    #def test_submit(self):
    #    js = "document.getElementById('msg').innerHTML = 'submit'"
    #    snippet = "<div id='msg'></div><form onSubmit=\"%s\"><input></input></form>" % js
    #    self.driver.open(snippet).find('input').submit()
    #    self.assertEqual(self.driver.find(id='msg').text, 'submit')

    #def test_submit(self):
    #    snippet = "<form onSubmit=\"alert('submit')\"><input></input></form>"
    #    self.driver.open(snippet).find('input').submit()
    #    self.assertEqual(self.driver.alert.text, 'submit')


WAIT_SNIPPET = """<html>
    <head>
        <script type="text/javascript">
addTextLater = function() {
    setTimeout(addText, 1000);
}
addText = function () {
    var txtNode = document.createTextNode("Hello World!");
    var p = document.getElementById("mypara");
    p.appendChild(txtNode);
}
        </script>
    </head>
    <body onload="addTextLater();">
        <p id="mypara"></p>
    </body>
</html>"""


class WaitTests(WebDriverPlusTests):
    extra_webdriver_kwargs = {'wait': 10}

    def setUp(self):
        super(WaitTests, self).setUp()
        snippet = WAIT_SNIPPET
        self.driver.open(snippet)

    def test_element_added_after_load_found(self):
        nodes = self.driver.find('p', text_contains='Hello World')
        self.assertEqual(len(nodes), 1)


class NoWaitTests(WebDriverPlusTests):
    def setUp(self):
        super(NoWaitTests, self).setUp()
        snippet = WAIT_SNIPPET
        self.driver.open(snippet)

    def test_element_added_after_load_not_found(self):
        nodes = self.driver.find('p', text_contains='Hello World')
        self.assertEqual(len(nodes), 0)


class ClassWithDeprecations(object):
    @webdriverplus.deprecation.deprecated_property
    def true(self):
        return True

    @webdriverplus.deprecation.deprecated_property
    def false(self):
        return False


class DeprecationWarningTests(unittest.TestCase):
    def setUp(self):
        webdriverplus.deprecation.WARN_ONLY = True

    def test_calling(self):
        instance = ClassWithDeprecations()
        with warnings.catch_warnings(record=True) as caught:
            self.assertTrue(instance.true())
            self.assertEqual(instance.true(), True)
            self.assertFalse(instance.false())
            self.assertEqual(instance.false(), False)
        self.assertEqual(len(caught), 0)

    def test_eq_prop(self):
        instance = ClassWithDeprecations()
        with warnings.catch_warnings(record=True) as caught:
            self.assertEqual(instance.false, False)
        self.assertEqual(len(caught), 1)

    def test_bool_prop(self):
        instance = ClassWithDeprecations()
        with warnings.catch_warnings(record=True) as caught:
            self.assertTrue(instance.true)
        self.assertEqual(len(caught), 1)


class DeprecationErrorTests(unittest.TestCase):
    def setUp(self):
        webdriverplus.deprecation.WARN_ONLY = False

    def test_calling(self):
        instance = ClassWithDeprecations()
        self.assertTrue(instance.true())
        self.assertEqual(instance.true(), True)
        self.assertFalse(instance.false())
        self.assertEqual(instance.false(), False)

    def test_eq_prop(self):
        instance = ClassWithDeprecations()
        self.assertRaises(
            webdriverplus.deprecation.DeprecatedPropertyError,
            lambda: not instance.false
        )

    def test_bool_prop(self):
        instance = ClassWithDeprecations()
        self.assertRaises(
            webdriverplus.deprecation.DeprecatedPropertyError,
            lambda: instance.true == True
        )
        self.assertRaises(
            webdriverplus.deprecation.DeprecatedPropertyError,
            lambda: instance.true != False
        )


if __name__ == '__main__':
    try:
        sys.argv.remove('--all')
    except:
        pass

    try:
        idx = sys.argv.index('--browser')
        browser = sys.argv[idx + 1]
        sys.argv.pop(idx)
        sys.argv.pop(idx)
    except:
        pass

    # If --headless argument is given, run headless in virtual session
    # using Xvfb or Xvnc.
    try:
        sys.argv.remove('--headless')
    except ValueError:
        pass
    else:
        try:
            from pyvirtualdisplay import Display
            from easyprocess import EasyProcessCheckInstalledError
        except ImportError:
            print('Error: --headless mode requires pyvirtualdisplay')
            sys.exit(2)
        try:
            display = Display(visible=0, size=(800, 600))
        except EasyProcessCheckInstalledError:
            print('Error: Could not initialize virtual display. ',
                  'Is either Xvfb or Xvnc installed?')
            sys.exit(2)
        print('Running tests in headless mode.')
        display.start()

    unittest.main()

    if 'display' in locals():
        display.stop()
