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
            lambda self, val: (By.ID, val),
        'xpath':
            lambda self, val: (By.XPATH, val),
        'name':
            lambda self, val: (By.NAME, val),
        'tag_name':
            lambda self, val: (By.TAG_NAME, val),
        'class_name':
            lambda self, val: (By.CLASS_NAME, val),
        'css':
            lambda self, val: (By.CSS_SELECTOR, val),
        'link_text':
            lambda self, val: (By.LINK_TEXT, val),
        'link_text_contains':
            lambda self, val: (By.PARTIAL_LINK_TEXT, val),
        'attribute':
            lambda self, val: (By.XPATH, '%s[@%s]' % (self._xpath_prefix, val)),
        'attribute_value':
            lambda self, val: (By.XPATH,
                         '%s[@%s=%s]' % (self._xpath_prefix, val[0], xpath_literal(val[1]))),
        'text':
            lambda self, val: (By.XPATH,
                         '%s[text()=%s]' % (self._xpath_prefix, xpath_literal(val))),
        'text_contains':
            lambda self, val: (By.XPATH,
                         '%s[contains(text(),%s)]' % (self._xpath_prefix, xpath_literal(val))),
        #'label':
        #    lambda self, val: (By.XPATH,
        #                 '//*[@id=//label[text()=%s]/@for]' % xpath_literal(val)),
        #'label_contains':
        #    lambda self, val: (By.XPATH,
        #                 '//*[@id=//label[contains(text(),%s)]/@for]' % xpath_literal(val)),
        'value':
            lambda self, val: (By.XPATH,
                         '%s[@value=%s]' % (self._xpath_prefix, xpath_literal(val))),
        'type':
            lambda self, val: (By.XPATH,
                         '%s[@type=%s]' % (self._xpath_prefix, xpath_literal(val))),
        'checked':
            lambda self, val: (By.XPATH,
                         self._xpath_prefix + ('[@checked]' if val else '[not(@checked)]')),
        'selected':
            lambda self, val: (By.XPATH,
                         self._xpath_prefix + ('[@selected]' if val else '[not(@selected)]')),
        # TODO: label, label_contains
    }

    def _get_selector(self, **kwargs):
        for arg, value in kwargs.items():
            func = self._ARG_TO_SELECTOR.get(arg, None)
            assert func, "'%s' is not a valid selector argument." % arg
            yield func(self, value)  # (selector, value) tuple

    def find(self, css=None, **kwargs):
        if css:
            kwargs['css'] = css
        assert kwargs, 'no selector argument supplied.'

        elems = None
        for selector, value in self._get_selector(**kwargs):
            if elems is not None:
                other = self.find_elements(by=selector, value=value)
                elems &= other
            else:
                elems = self.find_elements(by=selector, value=value)
        return elems

    #def find_all(self, css=None, **kwargs):
    #    (selector, value) = self._get_selector(css, **kwargs)
    #    return self.find_elements(by=selector, value=value)
