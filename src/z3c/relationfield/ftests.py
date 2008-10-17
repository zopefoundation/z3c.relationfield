import unittest

import grok

import zope.interface

from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds

from zc.relation.interfaces import ICatalog

from z3c.relationfield.interfaces import IHasRelations
from z3c.relationfield import Relation, RelationCatalog

from zope.app.testing.functional import FunctionalDocFileSuite
from z3c.relationfield.testing import FunctionalLayer

class IItem(zope.interface.Interface):
    """Test fixture used by README.txt
    """
    rel = Relation(title=u"Relation")
 
class Item(grok.Model):
    """Test fixture used by README.txt
    """
    grok.implements(IItem, IHasRelations)

    def __init__(self):
        self.rel = None

class TestApp(grok.Application, grok.Container):
    """Test fixture used by README.txt.
    """
    grok.local_utility(IntIds, provides=IIntIds)
    grok.local_utility(RelationCatalog, provides=ICatalog)
  
def test_suite():
    globs = { 'TestApp': TestApp, 'IItem': IItem, 'Item': Item }
    readme = FunctionalDocFileSuite(
        'README.txt',
        globs = globs,
        )
    readme.layer = FunctionalLayer
    return unittest.TestSuite([readme])
