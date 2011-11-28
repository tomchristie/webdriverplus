from selenium.webdriver.common.by import By


def xpath_literal(s):
    """
    http://stackoverflow.com/questions/6937525/escaping-xpath-literal-with-python
    """
    if "'" not in s:
        return "'%s'" % s
    if '"' not in s:
        return '"%s"' % s
    return "concat('%s')" % s.replace("'", "',\"'\",'")


class SelectorMixin(object):
    _ARG_TO_SELECTOR = {
        'id':
            lambda val: (By.ID, val),
        'xpath':
            lambda val: (By.XPATH, val),
        'name':
            lambda val: (By.NAME, val),
        'tag_name':
            lambda val: (By.TAG_NAME, val),
        'class_name':
            lambda val: (By.CLASS_NAME, val),
        'css':
            lambda val: (By.CSS_SELECTOR, val),
        'link':
            lambda val: (By.LINK_TEXT, val),
        'link_contains':
            lambda val: (By.PARTIAL_LINK_TEXT, val),
        'attribute':
            lambda val: (By.XPATH, '//*[@%s]' % val),
        'attribute_value':
            lambda val: (By.XPATH,
                         '//*[@%s=%s]' % (val[0], xpath_literal(val[1]))),
        'text':
            lambda val: (By.XPATH,
                         '//*[text()=%s]' % xpath_literal(val)),
        'text_contains':
            lambda val: (By.XPATH,
                         '//*[contains(text(),%s)]' % xpath_literal(val)),
        # TODO: label, label_contains
    }

    def _get_selector(self, css=None, **kwargs):
        if css:
            kwargs['css'] = css
        assert len(kwargs) == 1, 'no selector argument supplied.'

        arg, value = kwargs.items()[0]
        func = self._ARG_TO_SELECTOR.get(arg, None)
        assert func, "'%s' is not a valid selector argument." % arg
        selector, value = func(value)

        return (selector, value)

    def find(self, css=None, **kwargs):
        (selector, value) = self._get_selector(css, **kwargs)
        return self.find_element(by=selector, value=value)

    def find_all(self, css=None, **kwargs):
        (selector, value) = self._get_selector(css, **kwargs)
        return self.find_elements(by=selector, value=value)
