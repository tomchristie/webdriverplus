import unittest2 as unittest
import webdriverplus

driver = None


def setUpModule():
    global driver
    driver = webdriverplus.Firefox()


def tearDownModule():
    global driver
    driver.close()

# WebElements as set

# close_on_shutdown
# default_selector
# base_url

# drag & drop


class DriverTests(unittest.TestCase):
    def setUp(self):
        super(DriverTests, self).setUp()
        self.driver = driver

    #def test_get_file(self):
    #    page_text = 'abc'
    #    with tempfile.NamedTemporaryFile() as temp:
    #        temp.write(page_text)
    #        temp.flush()
    #        self.driver.get_file(temp.name)
    #    self.assertEquals(self.driver.page_text,  page_text)

    def test_open(self):
        page_text = 'abc'
        self.driver.open(page_text)
        self.assertEquals(self.driver.page_text,  page_text)

    def test_find(self):
        self.driver.open('<h1>123</h1><h2>456</h2><h3>789</h3>')
        self.assertEquals(self.driver.find('h2').text, '456')

    def test_find_all(self):
        self.driver.open('<h1>123</h1><h2>456</h2><h2>789</h2>')
        self.assertEquals(self.driver.find_all('h2').text, ['456', '789'])


class SelectorTests(unittest.TestCase):
    def setUp(self):
        super(SelectorTests, self).setUp()
        self.driver = driver
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
                         <form>
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

    # def test_label(self):
    #     node = self.driver.find(label='Password:')
    #     expected = '<input type="password" name="password" />'
    #     self.assertEquals(node.html, expected)

    # def test_label_contains(self):
    #     node = self.driver.find(label_contains='Password')
    #     expected = '<input type="password" name="password" />'
    #     self.assertEquals(node.html, expected)

    def test_attribute(self):
        node = self.driver.find(attribute='checked')
        self.assertEquals(node.value, 'blue')

    def test_attribute_value(self):
        node = self.driver.find(attribute_value=('checked', 'yes'))
        self.assertEquals(node.value, 'blue')

    # TODO: checked=True, checked=False, selected=True, selected=False


class TreeTraversalTests(unittest.TestCase):
    def setUp(self):
        super(TreeTraversalTests, self).setUp()
        self.driver = driver
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
        self.assertEquals(nodes.text, ['1', '2', '3', '4', '5'])

    def test_parent(self):
        node = self.driver.find('.selected').parent
        self.assertEquals(node.tag_name, 'ul')

    def test_descendants(self):
        nodes = self.driver.find('ul').descendants
        self.assertEquals(nodes.tag_names,
                          ['li', 'li', 'li', 'li', 'li', 'strong'])

    def test_next(self):
        node = self.driver.find('.selected').next
        self.assertEquals(node.text, '4')

    def test_prev(self):
        node = self.driver.find('.selected').prev
        self.assertEquals(node.text, '2')

    def test_next_all(self):
        nodes = self.driver.find('.selected').next_all
        self.assertEquals(nodes.text, ['4', '5'])

    def test_prev_all(self):
        nodes = self.driver.find('.selected').prev_all
        self.assertEquals(nodes.text, ['1', '2'])

    def test_siblings(self):
        nodes = self.driver.find('.selected').siblings
        self.assertEquals(nodes.text, ['1', '2', '4', '5'])


class ShortcutTests(unittest.TestCase):
    def setUp(self):
        super(ShortcutTests, self).setUp()
        self.driver = driver
        snippet = """<html>
                         <ul>
                             <li>1</li>
                             <li>2</li>
                             <li class="selected">3</li>
                             <li>4</li>
                             <li>5</li>
                         </ul>
                     </html>"""
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


class InspectionTests(unittest.TestCase):
    def setUp(self):
        super(InspectionTests, self).setUp()
        self.driver = driver
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


class ValueTests(unittest.TestCase):
    def setUp(self):
        super(ValueTests, self).setUp()
        self.driver = driver
        snippet = """<html>
                         <form>
                             <input type="text" name="username" value="mike">
                         </form>
                     </html>"""
        self.driver.open(snippet)

    def test_get_value(self):
        pass

    def test_set_value(self):
        pass


class SetTests(unittest.TestCase):
    def setUp(self):
        super(SetTests, self).setUp()
        self.driver = driver
        snippet = """<html>
                         <ul>
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
                         </ul>
                     </html>"""
        self.driver.open(snippet)

    def test_set_uniqueness(self):
        nodes = self.driver.find_all('li')
        self.assertEquals(len(nodes), 8)
        self.assertEquals(len(nodes.parent), 2)


if __name__ == '__main__':
    unittest.main()
