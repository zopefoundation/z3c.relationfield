import doctest
import re
import sys
import unittest

import six

from zope.component.testlayer import ZCMLFileLayer


# Evil hack to make pickling work with classes defined in doc tests
class NoCopyDict(dict):
    def copy(self):
        return self


class Py23DocChecker(doctest.OutputChecker):

    def check_output(self, want, got, optionflags):
        if six.PY2:
            want = re.sub("b'(.*?)'", "'\\1'", want)
        else:
            want = re.sub("u'(.*?)'", "'\\1'", want)

        return doctest.OutputChecker.check_output(self, want, got, optionflags)


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
        'README.rst',
        globs=globs,
        setUp=setUp,
        tearDown=tearDown,
        optionflags=doctest.ELLIPSIS,
        checker=Py23DocChecker(),
    )
    import z3c.relationfield
    readme.layer = ZCMLFileLayer(z3c.relationfield)
    return unittest.TestSuite([readme])
