from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.firefox.webdriver import WebDriver as _Firefox
from selenium.webdriver.chrome.webdriver import WebDriver as _Chrome
from selenium.webdriver.ie.webdriver import WebDriver as _Ie
from selenium.webdriver.remote.webdriver import WebDriver as _Remote
from selenium.webdriver.phantomjs.webdriver import WebDriver as _PhantomJS

from webdriverplus.utils import _download
from webdriverplus.webdriver import WebDriverMixin
from webdriverplus.webelement import WebElement

import atexit
import os
import socket
import subprocess
import time
try:
    from urllib2 import URLError
except ImportError:
    from urllib.error import URLError

VERSION = (0, 1, 5)


def get_version():
    return '%d.%d.%d' % (VERSION[0], VERSION[1], VERSION[2])


class WebDriver(WebDriverMixin):
    _pool = {}  # name -> (instance, signature)
    _quit_on_exit = set()  # set of instances
    _selenium_server = None  # Popen object
    _default_browser = 'firefox'

    @classmethod
    def _at_exit(cls):
        """
        Gets registered to run on system exit.
        """
        if cls._selenium_server:
            cls._selenium_server.kill()

        for driver in cls._quit_on_exit:
            try:
                driver.quit(force=True)
            except URLError:
                pass

    @classmethod
    def _get_from_pool(cls, browser):
        """Returns (instance, (args, kwargs))"""
        return cls._pool.get(browser, (None, (None, None)))

    def __new__(cls, browser=None, *args, **kwargs):
        browser = browser or cls._default_browser
        quit_on_exit = kwargs.get('quit_on_exit', True)
        reuse_browser = kwargs.get('reuse_browser')
        signature = (args, kwargs)
        browser = browser.lower()

        pooled_browser, pooled_signature = WebDriver._get_from_pool(browser)

        reused_pooled_browser = False

        if pooled_signature == signature:
            driver = pooled_browser
            reused_pooled_browser = True
        elif browser == 'firefox':
            driver = Firefox(*args, **kwargs)
        elif browser == 'chrome':
            driver = Chrome(*args, **kwargs)
        elif browser == 'ie':
            driver = Ie(*args, **kwargs)
        elif browser == 'remote':
            driver = Remote(*args, **kwargs)
        elif browser == 'phantomjs':
            driver = PhantomJS(*args, **kwargs)
        elif browser == 'htmlunit':
            driver = HtmlUnit(*args, **kwargs)

        if reuse_browser and not reused_pooled_browser:
            if pooled_browser:
                pooled_browser.quit(force=True)
            WebDriver._pool[browser] = (driver, signature)

        if quit_on_exit:
            WebDriver._quit_on_exit.add(driver)

        return driver

    def __init__(self, browser='firefox', *args, **kwargs):
        pass
        # Not actually called.  Here for autodoc purposes only.

atexit.register(WebDriver._at_exit)


class Firefox(WebDriverMixin, _Firefox):
    pass


class Chrome(WebDriverMixin, _Chrome):
    pass


class Ie(WebDriverMixin, _Ie):
    pass


class Remote(WebDriverMixin, _Remote):
    pass


class PhantomJS(WebDriverMixin, _PhantomJS):
    pass


class HtmlUnit(WebDriverMixin, _Remote):
    _selenium = 'selenium-server-standalone-2.22.0.jar'
    _selenium_url = 'http://selenium.googlecode.com/files/' + _selenium
    _auto_install = True

    def __init__(self, *args, **kwargs):
        self._perform_auto_install()
        self._autorun_selenium_server()
        super(HtmlUnit, self).__init__("http://localhost:4444/wd/hub",
                                       DesiredCapabilities.HTMLUNIT, **kwargs)

    def _create_web_element(self, element_id):
        return HtmlUnitWebElement(self, element_id)

    def _get_webdriver_dir(self):
        directory = os.path.expanduser('~/.webdriverplus')
        if not os.path.exists(directory):
            os.mkdir(directory)
        return directory

    def _get_selenium_path(self):
        return self._get_webdriver_dir() + '/' + self._selenium

    def _perform_auto_install(self):
        if not self._auto_install:
            return

        selenium_server = self._get_selenium_path()
        if not os.path.exists(selenium_server):
            _download(self._selenium_url, selenium_server)

    def _autorun_selenium_server(self):
        if WebDriver._selenium_server:
            return

        if subprocess.call(['hash', 'java']) != 0:
            raise Exception('java does not appear to be installed.')

        fnull = open(os.devnull, 'w')
        args = ['java', '-jar', self._get_selenium_path()]
        WebDriver._selenium_server = subprocess.Popen(args, stdout=fnull, stderr=fnull)

        now = time.time()
        timeout = 10
        connected = False
        while time.time() - now < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(('127.0.0.1', 4444))
            except:
                time.sleep(0.2)
            else:
                sock.close()
                connected = True
                break

        if not connected:
            raise Exception('Could not connect to selenium server')


class HtmlUnitWebElement(WebElement):
    def descendants(self):
        # HtmlUnit adds self into descendants
        ret = super(HtmlUnitWebElement, self).descendants()
        ret.discard(self)
        return ret

    @property
    def inner_html(self):
        # Need to use JS to do inner_html with HtmlUnit.
        script = "return arguments[0].innerHTML;"
        return self._parent.execute_script(script, self)
