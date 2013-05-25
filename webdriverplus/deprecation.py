""" Descriptor to provide an upgrade path for promoting property methods
back to regular methods """

import warnings

WARN_ONLY = True

message = """This property has been replaced by a method in order to conform
with the Selenium API. Please use %s() instead
"""


class DeprecatedPropertyError(Exception):
    pass


class DeprecatedProperty(object):
    def __init__(self, instance, method):

        self.instance = instance
        self.method = method

    def call(self):
        return self.method(self.instance)

    def call_and_notify(self):
        method = self.method
        method_name = method.__name__
        if WARN_ONLY:
            warnings.warn(message % method_name)
            return self.call()
        else:
            raise DeprecatedPropertyError(message % method_name)

    def __call__(self):
        return self.call()

    def __nonzero__(self):
        value = self.call_and_notify()
        return bool(value)

    # Python3 support
    def __bool__(self):
        return self.__nonzero__()

    def __eq__(self, other):
        value = self.call_and_notify()
        return value == other

    def __ne__(self, other):
        return not (self == other)


class DeprecatedPropertyDescriptor(object):
    def __init__(self, method):
        self.method = method

    def __get__(self, instance, owner):
        return DeprecatedProperty(instance, self.method)


# to conform to @property lowercase naming convention
deprecated_property = DeprecatedPropertyDescriptor