from selenium.webdriver.firefox.webdriver import WebDriver as Firefox
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.ie.webdriver import WebDriver as Ie
from selenium.webdriver.remote.webdriver import WebDriver as Remote
from webdriverplus.webdriver import WebDriverMixin


class WebDriver(WebDriverMixin, Remote):
    _pool = {}  # name -> (instance, signature)

    @classmethod
    def _get_from_pool(self, browser):
        return WebDriver._pool.get(browser, (None, (None, None)))

    def __new__(self, browser='firefox', *args, **kwargs):

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

        return driver

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
