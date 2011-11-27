from webdriverplus.orderedset import OrderedSet
from webdriverplus.selectors import SelectorMixin
from webdriverplus.wrappers import Style, Attributes


class WebElementSet(SelectorMixin, OrderedSet):
    # Mirror the existing WebElement interface to make the `find_all` and
    # `find_elements*` methods chainable.
    def find(self, css=None, **kwargs):
        return WebElementSet([elem.find(css, **kwargs) for elem in self])

    def find_all(self, css=None, **kwargs):
        ret = WebElementSet()
        for elem in self:
            ret |= elem._find_all(css, **kwargs)
        return ret

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
        return WebElementSet([elem.parent for elem in self])

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
