import unittest

from zope.app.testing.setup import setUpTestAsModule, tearDownTestAsModule
from zope.app.testing.functional import FunctionalDocFileSuite
from z3c.relationfield.testing import FunctionalLayer

def setUp(test):
    setUpTestAsModule(test, name='__builtin__')

def test_suite():
    globs = {}
    readme = FunctionalDocFileSuite(
        'README.txt',
        globs = globs,
        setUp=setUp,
        tearDown=tearDownTestAsModule,
        )
    readme.layer = FunctionalLayer
    return unittest.TestSuite([readme])
