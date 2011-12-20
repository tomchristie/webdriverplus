#!/usr/bin/env python

import sys
import unittest

import webdriverplus

# WebElements as set

# close_on_shutdown
# default_selector
# base_url

# drag & drop

# find_all().find() is broken
# No such element exceptions need to be cleaner

run_slow_tests = '--all' in sys.argv


class WebDriverPlusTests(unittest.TestCase):
    def setUp(self):
        super(WebDriverPlusTests, self).setUp()
        self.driver = webdriverplus.WebDriver('firefox', reuse_browser=True)

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
            self.assertEquals(browser, other)

        def test_reuse_browser_unset(self):
            browser = webdriverplus.WebDriver('firefox')
            browser.quit()
            other = webdriverplus.WebDriver('firefox')
            self.assertNotEquals(browser, other)


class DriverTests(WebDriverPlusTests):
    def test_open(self):
        page_text = 'abc'
        self.driver.open(page_text)
        self.assertEquals(self.driver.page_text,  page_text)

    def test_find(self):
        self.driver.open('<h1>123</h1><h2>456</h2><h3>789</h3>')
        self.assertEquals(self.driver.find('h2').text, '456')



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
                         </ul>
                         <form>
                             <label for="username">Username:</label>
                             <input type="text" name="username" value="lucy"/>
                             <label for="password">Password:</label>
                             <input type="password" name="password" />
                         </form>
                         <form id="checkboxlist">
                             <input type="checkbox" value="red" />
                             <input type="checkbox" value="green" />
                             <input type="checkbox" value="blue" checked=yes />
                         </form>
                     </html>"""
        self.driver.open(snippet)

    def test_id(self):
        node = self.driver.find(id='mylist')
        self.assertEquals(node.tag_name, 'ul')

    def test_class_name(self):
        node = self.driver.find(class_name='selected')
        self.assertEquals(node.text, 'three')

    def test_tag_name(self):
        node = self.driver.find(tag_name='h1')
        self.assertEquals(node.text, 'header')

    def test_name(self):
        node = self.driver.find(name='username')
        self.assertEquals(node.tag_name, 'input')
        self.assertEquals(node.value, 'lucy')

    def test_css(self):
        node = self.driver.find(css='ul li.selected')
        self.assertEquals(node.text, 'three')

    def test_xpath(self):
        node = self.driver.find(xpath='//ul/li[@class="selected"]')
        self.assertEquals(node.text, 'three')

    def test_link(self):
        node = self.driver.find(link='four')
        self.assertEquals(node.tag_name, 'a')
        self.assertEquals(node.text, 'four')

    def test_link_contains(self):
        node = self.driver.find(link_contains='ou')
        self.assertEquals(node.tag_name, 'a')
        self.assertEquals(node.text, 'four')

    def test_text(self):
        self.assertEquals(self.driver.find(text='one').index, 0)
        self.assertEquals(self.driver.find(text='two').index, 1)
        self.assertEquals(self.driver.find(text='three').index, 2)

    def test_text_contains(self):
        self.assertEquals(self.driver.find(text_contains='ne').index, 0)
        self.assertEquals(self.driver.find(text_contains='tw').index, 1)
        self.assertEquals(self.driver.find(text_contains='hre').index, 2)

    #def test_label(self):
    #    node = self.driver.find(label='Password:')
    #    expected = '<input type="password" name="password" />'
    #    self.assertEquals(node.html, expected)

    #def test_label_contains(self):
    #    node = self.driver.find(label_contains='Password')
    #    expected = '<input type="password" name="password" />'
    #    self.assertEquals(node.html, expected)

    def test_attribute(self):
        node = self.driver.find(attribute='checked')
        self.assertEquals(node.value, 'blue')

    def test_attribute_value(self):
        node = self.driver.find(attribute_value=('checked', 'yes'))
        self.assertEquals(node.value, 'blue')

    def test_value(self):
        node = self.driver.find(value='blue')
        self.assertEquals(node.tag_name, 'input')
        self.assertEquals(node.type, 'checkbox')
        self.assertEquals(node.value, 'blue')

    def test_type(self):
        node = self.driver.find(type='checkbox')
        self.assertEquals(node.value, 'red')

    def test_checked(self):
        elem = self.driver.find(id='checkboxlist')
        self.assertEquals(len(elem.find(checked=True)), 1)
        self.assertEquals(len(elem.find(checked=False)), 2)

    # TODO: checked=True, checked=False, selected=True, selected=False


class TreeTraversalTests(WebDriverPlusTests):
    def setUp(self):
        super(TreeTraversalTests, self).setUp()
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

    def test_children(self):
        nodes = self.driver.find('ul').children
        text = [node.text for node in nodes]
        self.assertEquals(text, ['1', '2', '3', '4', '5'])

    def test_parent(self):
        node = self.driver.find('.selected').parent
        self.assertEquals(node.tag_name, 'ul')

    def test_descendants(self):
        nodes = self.driver.find('ul').descendants
        tag_names = [node.tag_name for node in nodes]
        self.assertEquals(tag_names, ['li', 'li', 'li', 'li', 'li', 'strong'])

    def test_ancestors(self):
        nodes = self.driver.find(class_name='selected').ancestors
        tag_names = [node.tag_name for node in nodes]
        self.assertEquals(tag_names, ['html', 'body', 'ul'])

    def test_next(self):
        node = self.driver.find('.selected').next
        self.assertEquals(node.text, '4')

    def test_prev(self):
        node = self.driver.find('.selected').prev
        self.assertEquals(node.text, '2')

    def test_next_all(self):
        nodes = self.driver.find('.selected').next_all
        text = [node.text for node in nodes]
        self.assertEquals(text, ['4', '5'])

    def test_prev_all(self):
        nodes = self.driver.find('.selected').prev_all
        text = [node.text for node in nodes]
        self.assertEquals(text, ['1', '2'])

    def test_siblings(self):
        nodes = self.driver.find('.selected').siblings
        text = [node.text for node in nodes]
        self.assertEquals(text, ['1', '2', '4', '5'])


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
        self.assertEquals([node.text for node in nodes], ['3', '5'])

    def test_exclude(self):
        nodes = self.driver.find('li').exclude('.selected')
        self.assertEquals([node.text for node in nodes], ['1', '2', '4'])


class ShortcutTests(WebDriverPlusTests):
    def setUp(self):
        super(ShortcutTests, self).setUp()
        snippet = """<ul>
                         <li>1</li>
                         <li>2</li>
                         <li class="selected">3</li>
                         <li>4</li>
                         <li>5</li>
                     </ul>"""
        self.driver.open(snippet)

    def test_index(self):
        node = self.driver.find('.selected')
        self.assertEquals(node.index, 2)

    def test_html(self):
        node = self.driver.find('.selected')
        self.assertEquals(node.html, '<li class="selected">3</li>')

    def test_inner_html(self):
        node = self.driver.find('.selected')
        self.assertEquals(node.inner_html, '3')


class InspectionTests(WebDriverPlusTests):
    def setUp(self):
        super(InspectionTests, self).setUp()
        snippet = """<html>
                         <head>
                             <style type="text/css">
                                 .selected {color: red}
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
        self.assertEquals(elem.style.color, '#0000ff')

    def test_get_style_css(self):
        elem = self.driver.find('.selected')
        self.assertEquals(elem.style.color, '#ff0000')

    def test_set_style(self):
        elem = self.driver.find('.selected')
        elem.style.color = 'green'
        self.assertEquals(elem.style.color, '#008000')

    def test_size(self):
        elem = self.driver.find('img')
        self.assertEquals(elem.size.width, 100)
        self.assertEquals(elem.size.height, 50)

    def test_size_unpacked(self):
        (width, height) = self.driver.find('img').size
        self.assertEquals(width, 100)
        self.assertEquals(height, 50)

    def test_attributes(self):
        elem = self.driver.find('img')
        self.assertEquals(elem.attributes,
                          {'width': '100px', 'height': '50px', 'src': '#'})
        self.assertEquals(set(elem.attributes.keys()),
                          set(['width', 'height', 'src']))
        self.assertEquals(set(elem.attributes.values()),
                          set(['100px', '50px', '#']))

    def test_get_attribute(self):
        elem = self.driver.find('img')
        self.assertEquals(elem.attributes['width'], '100px')

    def test_set_attribute(self):
        elem = self.driver.find('img')
        elem.attributes['width'] = '33px'
        self.assertEquals(elem.attributes['width'], '33px')

    def test_del_attribute(self):
        elem = self.driver.find('img')
        del elem.attributes['src']
        self.assertEquals(elem.attributes,
                          {'width': '100px', 'height': '50px'})


class FormInspectionTests(WebDriverPlusTests):
    def setUp(self):
        super(FormInspectionTests, self).setUp()
        snippet = """<html>
                         <form>
                             <select>
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
        self.assertEquals(elem.find(text='Walk').is_selected, True)
        self.assertEquals(elem.find(text='Cycle').is_selected, False)
        self.assertEquals(elem.find(text='Drive').is_selected, False)

    def test_is_checked(self):
        elem = self.driver.find('form')
        self.assertEquals(elem.find(value='peanuts').is_checked, False)
        self.assertEquals(elem.find(value='jam').is_checked, True)


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
        self.assertEquals(len(nodes), 8)
        self.assertEquals(len(nodes.parent), 2)


if __name__ == '__main__':
    try:
        sys.argv.remove('--all')
    except:
        pass
    unittest.main()
