import unittest

import grok

import zope.interface

from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds

from z3c.relationfield.index import RelationCatalog
from z3c.relationfield.interfaces import IHasRelations
from z3c.relationfield import schema

import zope.testbrowser.browser
import zope.testbrowser.testing
from zope.app.testing.functional import FunctionalDocFileSuite
from z3c.relationfield.testing import FunctionalLayer

class IItem(zope.interface.Interface):
    rel = schema.Relation(title=u"Relation")
 
class Item(grok.Model):
    grok.implements(IItem, IHasRelations)

    def __init__(self):
        self.rel = None

class TestApp(grok.Application, grok.Container):
    grok.local_utility(IntIds, provides=IIntIds)
    grok.local_utility(RelationCatalog)
  
def test_suite():
    globs = { 'TestApp': TestApp, 'IItem': IItem, 'Item': Item }
    readme = FunctionalDocFileSuite(
        'README.txt',
        globs = globs,
        )
    readme.layer = FunctionalLayer
    return unittest.TestSuite([readme])
