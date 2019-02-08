from z3c.relationfield.interfaces import IRelationValue
from zc.relation.catalog import Catalog
from zope import component
from zope.intid.interfaces import IIntIds

import BTrees

DEFAULT_INDEXES = [
    {
        'element': IRelationValue['from_id'],
    },
    {
        'element': IRelationValue['to_id'],
    },
    {
        'element': IRelationValue['from_attribute'],
        'kwargs': {
            'btree': BTrees.family32.OI,
        },
    },
    {
        'element': IRelationValue['from_interfaces_flattened'],
        'kwargs': {
            'btree': BTrees.family32.OI,
            'multiple': True,
        },
    },
    {
        'element': IRelationValue['to_interfaces_flattened'],
        'kwargs': {
            'btree': BTrees.family32.OI,
            'multiple': True,
        },
    },
]


def dump(obj, catalog, cache):
    intids = cache.get('intids')
    if intids is None:
        intids = cache['intids'] = component.getUtility(IIntIds)
    return intids.getId(obj)


def load(token, catalog, cache):
    intids = cache.get('intids')
    if intids is None:
        intids = cache['intids'] = component.getUtility(IIntIds)
    return intids.getObject(token)


class RelationCatalog(Catalog):

    def __init__(self, indexes=DEFAULT_INDEXES):
        """Initialize the catalog with indexes.

        Uses defaults if not special configuration was passed.
        """
        Catalog.__init__(self, dump, load)
        for index in indexes:
            self.addValueIndex(index['element'], **index.get('kwargs', {}))
