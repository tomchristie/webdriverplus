from webdriverplus.webelement import WebElement
from webdriverplus.webelementset import WebElementSet
from webdriverplus.selectors import SelectorMixin
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

import re
import tempfile

from selenium.common.exceptions import StaleElementReferenceException


class WebDriverMixin(SelectorMixin):
    def __init__(self, *args, **kwargs):
        self.reuse_browser = kwargs.pop('reuse_browser', False)
        self.quit_on_exit = kwargs.pop('quit_on_exit', False)
        self.wait = kwargs.pop('wait', 0)
        self.highlight = kwargs.pop('highlight', True)
        self._highlighted = None
        self._has_quit = False
        super(WebDriverMixin, self).__init__(*args, **kwargs)

    def quit(self, force=False):
        if self._has_quit:
            return
        if self.reuse_browser and not force:
            # alert = self.alert
            # if alert:
            #     alert.dismiss()
            return
        super(WebDriverMixin, self).quit()
        self._has_quit = True

    def _highlight(self, elems):
        if not self.highlight:
            return
        if self._highlighted:
            script = """for (var i = 0, j = arguments.length; i < j; i++) {
                            var elem = arguments[i];
                            elem.style.backgroundColor = elem.getAttribute('savedBackground');
                            elem.style.borderColor = elem.getAttribute('savedBorder');
                            elem.style.outline = elem.getAttribute('savedOutline');
                        }"""
            try:
                self.execute_script(script, *self._highlighted)
            except StaleElementReferenceException:
                pass

        self._highlighted = elems
        script = """
            for (var i = 0, j = arguments.length; i < j; i++) {
                var elem = arguments[i];
                elem.setAttribute('savedBackground', elem.style.backgroundColor);
                elem.setAttribute('savedBorder', elem.style.borderColor);
                elem.setAttribute('savedOutline', elem.style.outline);
                elem.style.backgroundColor = '#f9edbe'
                elem.style.borderColor = '#f9edbe'
                elem.style.outline = '1px solid black';
            }"""
        try:
            self.execute_script(script, *elems)
        except StaleElementReferenceException:
            pass

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
        if not re.match("[^<]*<(html|doctype)", content, re.IGNORECASE):
            content = '<html><head><meta charset="utf-8"></head>%s</html>' % content
        with tempfile.NamedTemporaryFile() as temp:
            temp.write(content.encode('utf-8'))
            temp.flush()
            return self.get('file://' + temp.name)

    @property
    def page_text(self):
        """
        Returns the full page text.
        """
        return self.find(tag_name='body').text

    @property
    def alert(self):
        alert = self.switch_to_alert()
        try:
            alert.text
        except:
            return None
        return alert

    def switch_to_frame(self, frame):
        if isinstance(frame, WebElementSet):
            return super(WebDriverMixin, self).switch_to_frame(frame._first)
        return super(WebDriverMixin, self).switch_to_frame(frame)

    def __repr__(self):
        return '<WebDriver Instance, %s>' % (self.name)
