from selenium.webdriver.firefox.webdriver import WebDriver as Firefox
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.ie.webdriver import WebDriver as Ie
from selenium.webdriver.remote.webdriver import WebDriver as Remote
from webdriverplus.webdriver import WebDriverMixin


class WebDriver(WebDriverMixin, Remote):
    def __new__(self, browser='firefox', *args, **kwargs):
        browser = browser.lower()
        if browser == 'firefox':
            return Firefox(*args, **kwargs)
        elif browser == 'chrome':
            return Chrome(*args, **kwargs)
        elif browser == 'ie':
            return Ie(*args, **kwargs)
        elif browser == 'remote':
            return Remote(*args, **kwargs)

    def __init__(self, browser='firefox', *args, **kwargs):
        pass
        # Not actually called.  Here for autodoc purposes only.


class Firefox(WebDriverMixin, Firefox):
    pass


class Chrome(WebDriverMixin, Chrome):
    pass


class Ie(WebDriverMixin, Ie):
    pass


class Remote(WebDriverMixin, Remote):
    pass
