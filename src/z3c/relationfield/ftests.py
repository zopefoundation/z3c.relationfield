from zope.component.testlayer import ZCMLFileLayer
import doctest
import sys
import unittest


# Evil hack to make pickling work with classes defined in doc tests
class NoCopyDict(dict):
    def copy(self):
        return self


class FakeModule:
    """A fake module."""

    def __init__(self, dict):
        self.__dict = dict

    def __getattr__(self, name):
        try:
            return self.__dict[name]
        except KeyError:
            raise AttributeError(name)


def setUp(test):
    test.globs['__name__'] = '__builtin__'
    test.globs = NoCopyDict(test.globs)
    sys.modules['__builtin__'] = FakeModule(test.globs)


def tearDown(test):
    del sys.modules['__builtin__']
    test.globs.clear()


def test_suite():
    globs = {}
    readme = doctest.DocFileSuite(
        'README.txt',
        globs=globs,
        setUp=setUp,
        tearDown=tearDown,
        optionflags=doctest.ELLIPSIS,
    )
    import z3c.relationfield
    readme.layer = ZCMLFileLayer(z3c.relationfield)
    return unittest.TestSuite([readme])
