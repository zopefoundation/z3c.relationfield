import unittest

from persistent import Persistent

import zope.interface

from zope.interface import implements
from zope.app.component.site import SiteManagerContainer
from zope.app.container.btree import BTreeContainer

from zc.relation.interfaces import ICatalog

from z3c.relationfield.interfaces import IHasRelations
from z3c.relationfield import Relation, RelationCatalog

from zope.app.testing.functional import FunctionalDocFileSuite
from z3c.relationfield.testing import FunctionalLayer

class IItem(zope.interface.Interface):
    """Test fixture used by README.txt
    """
    rel = Relation(title=u"Relation")
 
class Item(Persistent):
    """Test fixture used by README.txt
    """
    implements(IItem, IHasRelations)

    def __init__(self):
        self.rel = None

class TestApp(SiteManagerContainer, BTreeContainer):
    """Test fixture used by README.txt.
    """
    pass

def test_suite():
    globs = { 'TestApp': TestApp, 'IItem': IItem, 'Item': Item }
    readme = FunctionalDocFileSuite(
        'README.txt',
        globs = globs,
        )
    readme.layer = FunctionalLayer
    return unittest.TestSuite([readme])
