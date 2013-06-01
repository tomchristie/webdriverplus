from selenium.webdriver.remote.webelement import WebElement as _WebElement
from webdriverplus.webelement import WebElement
from webdriverplus.webelementset import WebElementSet
from webdriverplus.selectors import SelectorMixin

import re
import tempfile
import inspect

from selenium.common.exceptions import StaleElementReferenceException


class WebDriverDecorator(SelectorMixin):
    def __init__(self, *args, **kwargs):
        self.reuse_browser = kwargs.pop('reuse_browser', False)
        self.quit_on_exit = kwargs.pop('quit_on_exit', False)
        self.wait = kwargs.pop('wait', 0)
        self.highlight = kwargs.pop('highlight', True)
        self._highlighted = None
        self._has_quit = False
        driver = kwargs.pop('driver', None)
        # If driver is a class, initialize it
        if driver is None:
            raise Exception('Need a WebDriver class or instance')
        if inspect.isclass(driver):
            self.driver = driver(*args, **kwargs)
        else:
            self.driver = driver

    def quit(self, force=False):
        if self._has_quit:
            return
        if self.reuse_browser and not force:
            # alert = self.alert
            # if alert:
            #     alert.dismiss()
            return
        self.driver.quit()
        self._has_quit = True

    def _get_driver(self):
        return self.driver

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
                self.driver.execute_script(script, *self._highlighted)
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
            self.driver.execute_script(script, *elems)
        except StaleElementReferenceException:
            pass

    @property
    def _xpath_prefix(self):
        return '//*'

    # Override the default behavior to return our own WebElement and
    # WebElements objects.

    def _create_web_element(self, element_id):
        return WebElement(self, element_id)

    def _create_web_elements(self, elements):
        return WebElementSet(self, elements)

    def _convert_value(self, value):
        if isinstance(value, _WebElement):
            return self._create_web_element(value.id)
        elif isinstance(value, list):
            return self._create_web_elements(self._create_web_element(elem.id) for elem in value)
        return value

    # Override get to return self
    def get(self, url):
        self.driver.get(url)
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
        alert = self.driver.switch_to_alert()
        try:
            alert.text
        except:
            return None
        return alert

    def switch_to_frame(self, frame):
        if isinstance(frame, WebElementSet):
            return self.driver.switch_to_frame(frame._first)
        return self.driver.switch_to_frame(frame)

    def execute(self, *args, **kwargs):
        resp = self.driver.execute(*args, **kwargs)
        resp['value'] = self._convert_value(resp.get('value', None))
        return resp

    def __getattr__(self, name):
        attr = getattr(self.driver, name)
        if name.startswith('find_'):
            def wrapper(*args, **kwargs):
                return self._convert_value(attr(*args, **kwargs))
            return wrapper
        return attr

    def __repr__(self):
        return '<WebDriverDecorator Instance, %s>' % self.driver.name
