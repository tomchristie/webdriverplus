from webdriverplus.orderedset import OrderedSet
from webdriverplus.selectors import SelectorMixin
from webdriverplus.wrappers import Style, Attributes
from webdriverplus.deprecation import deprecated_property


class WebElementSet(SelectorMixin, OrderedSet):
    def __init__(self, webdriver, *args):
        super(WebElementSet, self).__init__(*args)
        self._webdriver = webdriver

    def _from_iterable(self, it):
        return WebElementSet(self._webdriver, it)

    def _empty(self):
        return WebElementSet(self._webdriver)

    def find(self, css=None, **kwargs):
        ret = self._empty()
        for elem in self:
            ret |= elem.find(css, **kwargs)
        return ret

    #def find_all(self, css=None, **kwargs):
    #    ret = WebElementSet(self._webdriver)
    #    for elem in self:
    #        ret |= elem.find_all(css, **kwargs)
    #    return ret

    def filter(self, css=None, **kwargs):
        if not css or kwargs:
            return self
        others = self._webdriver.find(css, **kwargs)
        return self & others

    def exclude(self, css=None, **kwargs):
        others = self._webdriver.find(css, **kwargs)
        return self - others

    @property
    def tag_name(self):
        return self._first.tag_name

    @property
    def text(self):
        return self._first.text

    @deprecated_property
    def is_selected(self):
        return self._first.is_selected()

    @deprecated_property
    def is_enabled(self):
        return self._first.is_enabled()

    @deprecated_property
    def is_displayed(self):
        return self._first.is_displayed()

    @deprecated_property
    def is_checked(self):
        return self._first.is_checked()

    # Events...
    def click(self):
        self._first.click()
        return self

    def double_click(self):
        self._first.double_click()
        return self

    def context_click(self):
        self._first.context_click()
        return self

    def click_and_hold(self):
        self._first.click_and_hold()
        return self

    def release(self):
        self._first.release()
        return self

    def move_to(self, x=0, y=0):
        self._first.move_to(x, y)
        return self

    def move_to_and_click(self, *args, **kwargs):
        self._first.move_to_and_click(*args, **kwargs)
        return self

    def check(self):
        self._first.check()
        return self

    def uncheck(self):
        self._first.uncheck()
        return self

    def submit(self):
        self._first.submit()
        return self

    def clear(self):
        self._first.clear()
        return self

    #
    def get_attribute(self, name):
        return self._first.get_attribute(name)

    def attr(self, name):
        return self._first.attr(name)

    def send_keys(self, *value):
        [elem.send_keys(*value) for elem in self]
        return self

    @property
    def type(self):
        return self._first.type

    @property
    def inner_html(self):
        return self._first.inner_html

    @property
    def html(self):
        return self._first.html

    @property
    def index(self):
        return self._first.index

    @property
    def value(self):
        return self._first.value

    @value.setter
    def value(self, value):
        self._first.value = value
        
    def value_of_css_property(self, property_name):
        return [elem.value_of_css_property(property_name) for elem in self]

    @property
    def location(self):
        return self._first.location

    @property
    def size(self):
        return self._first.size

    @property
    def id(self):
        return self._first.id

    @property
    def style(self):
        return Style(self._first)

    @property
    def attributes(self):
        return Attributes(self._first)

    def has_class(self, cls):
        for elem in self:
            if elem.has_class(cls):
                return True
        return False

    def css(self, name, value=None):
        return self._first.css(name, value)

    def javascript(self, script):
        return [elem.javascript(script) for elem in self]

    def __repr__(self):
        ret = "WebElementSet(\n  %s\n)" % '\n  '.join([repr(elem) for elem in self])
        script = """for (var i = 0, j = arguments.length; i < j; i++) {
                        var style = arguments[i].style;
                        style.backgroundColor = '#f9edbe'
                        style.borderColor = '#f9edbe'
                        style.outline = '1px solid black';
                    }"""
        self._webdriver._highlight([elem for elem in self])
        return ret

    # Traversal
    def parent(self, *args, **kwargs):
        ret = self._empty()
        for elem in self:
            ret |= elem.parent()
        return ret.filter(*args, **kwargs)

    def children(self, *args, **kwargs):
        ret = self._empty()
        for elem in self:
            ret |= elem.children()
        return ret.filter(*args, **kwargs)

    def descendants(self):
        ret = self._empty()
        for elem in self:
            ret |= elem.descendants()
        return ret

    def ancestors(self, *args, **kwargs):
        ret = self._empty()
        for elem in self:
            ret |= elem.ancestors()
        return ret.filter(*args, **kwargs)

    def next(self, *args, **kwargs):
        ret = self._empty()
        for elem in self:
            ret |= elem.next()
        return ret.filter(*args, **kwargs)

    def prev(self, *args, **kwargs):
        ret = self._empty()
        for elem in self:
            ret |= elem.prev()
        return ret.filter(*args, **kwargs)

    def next_all(self, *args, **kwargs):
        ret = self._empty()
        for elem in self:
            ret |= elem.next_all()
        return ret.filter(*args, **kwargs)

    def prev_all(self, *args, **kwargs):
        ret = self._empty()
        for elem in self:
            ret |= elem.prev_all()
        return ret.filter(*args, **kwargs)

    def siblings(self, *args, **kwargs):
        ret = self._empty()
        for elem in self:
            ret |= elem.siblings()
        return ret.filter(*args, **kwargs)

    def type_keys(self, *args):
        return self._first.type_keys(*args)

    def select_option(self, value=None, text=None, index=None):
        return self._first.select_option(value=value, text=text, index=index)

    def deselect_option(self, value=None, text=None, index=None):
        return self._first.deselect_option(value=value, text=text, index=index)

    def __getitem__(self, key):
        if isinstance(key, slice):
            elems = list(self)[key]
        else:
            elems = [list(self)[key]]
        return WebElementSet(self._webdriver, elems)
