from webdriverplus.orderedset import OrderedSet
from webdriverplus.selectors import SelectorMixin
from webdriverplus.wrappers import Style, Attributes


class WebElementSet(SelectorMixin, OrderedSet):
    def __init__(self, webdriver, *args):
        super(WebElementSet, self).__init__(*args)
        self._webdriver = webdriver

    def _from_iterable(self, it):
        return WebElementSet(self._webdriver, it)

    # Mirror the existing WebElement interface to make the `find_all` and
    # `find_elements*` methods chainable.
    def find(self, css=None, **kwargs):
        return WebElementSet(self._webdriver,
                             [elem.find(css, **kwargs) for elem in self])

    def find_all(self, css=None, **kwargs):
        ret = WebElementSet(self._webdriver)
        for elem in self:
            ret |= elem.find_all(css, **kwargs)
        return ret

    def filter(self, css=None, **kwargs):
        others = self._webdriver.find_all(css, **kwargs)
        return self & others

    def exclude(self, css=None, **kwargs):
        others = self._webdriver.find_all(css, **kwargs)
        return self - others

    @property
    def tag_names(self):
        return [elem.tag_name for elem in self]

    @property
    def text(self):
        return [elem.text for elem in self]

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

    def is_selected(self):
        return [elem.is_selected() for elem in self]

    def is_enabled(self):
        return [elem.is_enabled for elem in self]

    def send_keys(self, *value):
        [elem.send_keys(*value) for elem in self]
        return self

    def is_displayed(self):
        return [elem.is_displayed() for elem in self]

    @property
    def size(self):
        return [elem.size for elem in self]

    def value_of_css_property(self, property_name):
        return [elem.value_of_css_property(property_name) for elem in self]

    @property
    def location(self):
        return [elem.location for elem in self]

    @property
    def parent(self):
        return WebElementSet(self._webdriver, [elem.parent for elem in self])

    @property
    def id(self):
        return [elem.id for elem in self]

    @property
    def style(self):
        return Style(self)

    @property
    def attributes(self):
        return Attributes(self)

    def javascript(self, script):
        return [elem.javascript(script) for elem in self]

    def __repr__(self):
        return "WebElementSet(\n  %s\n)" % '\n  '.join([repr(elem) for elem in self])
