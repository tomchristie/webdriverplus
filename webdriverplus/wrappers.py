from collections import namedtuple


Size = namedtuple('Size', ['width', 'height'])

Location = namedtuple('Location', ['x', 'y'])


class Style(object):
    """
    Allows getting and setting the CSS style.
    """
    _elem = None

    def __init__(self, elem):
        self.__dict__.update({'_elem': elem})

    def __getattr__(self, name):
        return self._elem.value_of_css_property(name)

    def __setattr__(self, name, value):
        self._elem.javascript('style.%s = "%s"' % (name, value))


# http://thatmattbone.com/2010/04/delaying-computation-lazy-dictionaries-in-python/
# http://stackoverflow.com/questions/2048720/get-all-attributes-from-a-html-element-with-javascript-jquery
class Attributes(object):
    """
    Allows getting, setting and deleting attributes.
    """

    def __init__(self, elem):
        self._elem = elem

    def _get_attributes(self):
        script = """
        var elem = arguments[0];
        var ret = {}
        for (var i=0, attrs=elem.attributes, l=attrs.length; i<l; i++){
            ret[attrs.item(i).nodeName] = attrs.item(i).nodeValue
        }
        return ret"""
        return self._elem._parent.execute_script(script, self._elem)

    def __getitem__(self, name):
        return self._elem.javascript("getAttribute('%s')" % name)

    def __setitem__(self, name, value):
        return self._elem.javascript("setAttribute('%s', %s)" %
                                     (name, repr(value)))

    def __delitem__(self, name):
        return self._elem.javascript("removeAttribute('%s')" % name)

    def __getattr__(self, name):
        data = self._get_attributes()
        return getattr(data, name)

    def __repr__(self):
        return repr(self._get_attributes())

    def __eq__(self, other):
        return self._get_attributes() == other
