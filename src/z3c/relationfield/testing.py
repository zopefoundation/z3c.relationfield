from zc.relation.interfaces import ICatalog
from zope.component import getGlobalSiteManager
from zope.component import provideUtility
from zope.interface import implementer
from zope.intid.interfaces import IIntIds

import z3c.relationfield


@implementer(IIntIds)
class MockIntIds:
    """Dumb utility for unit tests, returns sequential integers. Not a
    complete implementation."""

    def getId(self, ob):
        """Appropriately raises KeyErrors when the object is not registered,
        e.g. always"""
        raise KeyError(ob)


mock_intids = MockIntIds()


@implementer(ICatalog)
class MockCatalog:
    """Does nothing except exist"""

    def findRelations(self, query):
        return []


mock_catalog = MockCatalog()


def register_fake_intid():
    provideUtility(mock_intids)


def unregister_fake_intid():
    sm = getGlobalSiteManager()
    sm.unregisterUtility(mock_intids)


def register_fake_catalog():
    provideUtility(mock_catalog)


def unregister_fake_catalog():
    sm = getGlobalSiteManager()
    sm.unregisterUtility(mock_catalog)


@implementer(z3c.relationfield.interfaces.IHasRelations)
class MockContent:
    pass
