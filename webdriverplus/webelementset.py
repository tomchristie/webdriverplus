from webdriverplus.orderedset import OrderedSet
from webdriverplus.selectors import SelectorMixin
from webdriverplus.wrappers import Style, Attributes


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

    def click(self):
        [elem.click for elem in self]
        return self

    def submit(self):
        [elem.submit() for elem in self]
        return self

    def clear(self):
        [elem.clear() for elem in self]
        return self

    def get_attribute(self, name):
        return [elem.get_attribute(name) for elem in self]

    @property
    def is_selected(self):
        return self._first.is_selected

    @property
    def is_enabled(self):
        return self._first.is_enabled

    @property
    def is_displayed(self):
        return self._first.is_displayed

    @property
    def is_checked(self):
        return self._first.is_checked

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
    def innder_html(self):
        return self._first.size

    @property
    def value(self):
        return self._first.value

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
    @property
    def parent(self):
        ret = self._empty()
        for elem in self:
            ret |= elem.parent
        return ret

    @property
    def children(self):
        ret = self._empty()
        for elem in self:
            ret |= elem.children
        return ret

    @property
    def descendants(self):
        ret = self._empty()
        for elem in self:
            ret |= elem.descendants
        return ret

    @property
    def ancestors(self):
        ret = self._empty()
        for elem in self:
            ret |= elem.ancestors
        return ret

    @property
    def next(self):
        ret = self._empty()
        for elem in self:
            ret |= elem.next
        return ret

    @property
    def prev(self):
        ret = self._empty()
        for elem in self:
            ret |= elem.prev
        return ret

    @property
    def next_all(self):
        ret = self._empty()
        for elem in self:
            ret |= elem.next_all
        return ret

    @property
    def prev_all(self):
        ret = self._empty()
        for elem in self:
            ret |= elem.prev_all
        return ret

    @property
    def siblings(self):
        ret = self._empty()
        for elem in self:
            ret |= elem.siblings
        return ret
