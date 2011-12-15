from webdriverplus.webelement import WebElement
from webdriverplus.webelementset import WebElementSet
from webdriverplus.selectors import SelectorMixin

import tempfile


class WebDriverMixin(SelectorMixin):
    _has_quit = False

    def __init__(self, reuse_browser=False, quit_on_exit=True,
                 *args, **kwargs):
        super(WebDriverMixin, self).__init__(*args, **kwargs)
        self.reuse_browser = reuse_browser
        self.quit_on_exit = quit_on_exit

    def quit(self, force=False):
        if self._has_quit:
            return
        if self.reuse_browser and not force:
            return
        super(WebDriverMixin, self).quit()
        self._has_quit = True

    @property
    def _xpath_prefix(self):
        return '//*'

    # Override the default behavior to return our own WebElement and
    # WebElements objects.
    def _is_web_element(self, value):
        return isinstance(value, dict) and 'ELEMENT' in value

    def _is_web_element_list(self, lst):
        return all(isinstance(value, WebElement) for value in lst)

    def _create_web_element(self, element_id):
        return WebElement(self, element_id)

    def _create_web_elements(self, elements):
        return WebElementSet(self, elements)

    def _unwrap_value(self, value):
        if self._is_web_element(value):
            return self._create_web_element(value['ELEMENT'])
        elif isinstance(value, list):
            lst = [self._unwrap_value(item) for item in value]
            if self._is_web_element_list(lst):
                return self._create_web_elements(lst)
            return lst
        else:
            return value

    def _wrap_value(self, value):
        if isinstance(value, dict):
            converted = {}
            for key, val in value.items():
                converted[key] = self._wrap_value(val)
            return converted
        elif isinstance(value, WebElement):
            return {'ELEMENT': value._id}  # Use '._id', not '.id'
        elif isinstance(value, list):
            return list(self._wrap_value(item) for item in value)
        else:
            return value

    # Override get to return self
    def get(self, url):
        super(WebDriverMixin, self).get(url)
        return self

    # Add some useful shortcuts.
    def open(self, content):
        """
        Shortcut to open from text.
        """
        with tempfile.NamedTemporaryFile() as temp:
            temp.write(content)
            temp.flush()
            return self.get('file://' + temp.name)

    @property
    def page_text(self):
        """
        Returns the full page text.
        """
        return self.find(tag_name='body').text

    def __repr__(self):
        return 'WebDriver (%s) - %s' % (self.name, self.current_url)
