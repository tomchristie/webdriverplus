from selenium.webdriver.firefox.webdriver import WebDriver as Firefox
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.ie.webdriver import WebDriver as Ie
from selenium.webdriver.remote.webdriver import WebDriver as Remote
from webdriverplus.webdriver import WebDriver


class Firefox(WebDriver, Firefox):
    pass


class Chrome(WebDriver, Chrome):
    pass


class Ie(WebDriver, Ie):
    pass


class Remote(WebDriver, Remote):
    pass
