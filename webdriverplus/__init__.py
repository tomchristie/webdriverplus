from selenium.webdriver.firefox.webdriver import WebDriver as Firefox
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.ie.webdriver import WebDriver as Ie
from selenium.webdriver.remote.webdriver import WebDriver as Remote
from webdriverplus.webdriver import WebDriverMixin

import atexit
import urllib2

VERSION = (0, 0, 3, 'final')

assert(VERSION[3] in ('dev', 'final'))


def get_version():
    ret = '%d.%d.%d' % (VERSION[0], VERSION[1], VERSION[2])
    if VERSION[3] == 'dev':
        ret += ' development'
    return ret


class WebDriver(WebDriverMixin, Remote):
    _pool = {}  # name -> (instance, signature)
    _quit_on_exit = set()  # set of instances

    @classmethod
    def _at_exit(cls):
        for driver in cls._quit_on_exit:
            try:
                driver.quit(force=True)
            except urllib2.URLError:
                pass

    @classmethod
    def _get_from_pool(cls, browser):
        """Returns (instance, (args, kwargs))"""
        return cls._pool.get(browser, (None, (None, None)))

    def __new__(cls, browser='firefox', *args, **kwargs):

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


class Firefox(WebDriverMixin, Firefox):
    pass


class Chrome(WebDriverMixin, Chrome):
    pass


class Ie(WebDriverMixin, Ie):
    pass


class Remote(WebDriverMixin, Remote):
    pass
