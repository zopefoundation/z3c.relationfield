import z3c.relationfield
from zc.relation.interfaces import ICatalog
from zope.interface import implements
from zope.component import provideUtility, getGlobalSiteManager
from zope.intid.interfaces import IIntIds


class MockIntIds(object):
    """Dumb utility for unit tests, returns sequential integers. Not a
    complete implementation."""
    implements(IIntIds)

    def getId(self, ob):
        """Appropriately raises KeyErrors when the object is not registered,
        e.g. always"""
        raise KeyError(ob)
mock_intids = MockIntIds()


class MockCatalog(object):
    """Does nothing except exist"""
    implements(ICatalog)

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


class MockContent(object):
    implements(z3c.relationfield.interfaces.IHasRelations)
