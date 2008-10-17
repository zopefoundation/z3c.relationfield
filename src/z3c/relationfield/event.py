import grokcore.component as grok

from zope.interface import providedBy
from zope.schema import getFields
from zope import component
from zope.app.intid.interfaces import IIntIds
from zope.app.container.interfaces import (IObjectAddedEvent,
                                           IObjectRemovedEvent)
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from zc.relation.interfaces import ICatalog

from z3c.relationfield.interfaces import (IHasRelations,
                                          IRelation,
                                          IRelationValue,
                                          ITemporaryRelationValue)

@grok.subscribe(IHasRelations, IObjectAddedEvent)
def addRelations(obj, event):
    """Register relations.

    Any relation object on the object will be added.
    """
    for name, relation in _relations(obj):
         _setRelation(obj, name, relation)

@grok.subscribe(IHasRelations, IObjectRemovedEvent)
def removeRelations(obj, event):
    """Remove relations.

    Any relation object on the object will be removed from the catalog.
    """
    catalog = component.getUtility(ICatalog)
 
    for name, relation in _relations(obj):
        if relation is not None:
            catalog.unindex(relation)

@grok.subscribe(IHasRelations, IObjectModifiedEvent)
def updateRelations(obj, event):
    """Re-register relations, after they have been changed.
    """
    catalog = component.getUtility(ICatalog)
    intids = component.getUtility(IIntIds)

    # remove previous relations coming from id (now have been overwritten)
    for relation in catalog.findRelations({'from_id': intids.getId(obj)}):
        catalog.unindex(relation)    

    # add new relations
    addRelations(obj, event)

def realize_relations(obj):
    """Given an object, convert any temporary relatiosn on it to real ones.
    """
    for name, relation in _potential_relations(obj):
        if ITemporaryRelationValue.providedBy(relation):
            setattr(obj, name, relation.convert())

def _setRelation(obj, name, value):
    """Set a relation on an object.

    Sets up various essential attributes on the relation.
    """
    # if the Relation is None, we're done
    if value is None:
        return
    # make sure relation has a __parent__ so we can make an intid for it
    value.__parent__ = obj
    # also set from_object to parent object
    value.from_object = obj
    # and the attribute to the attribute name
    value.from_attribute = name
    # now we can create an intid for the relation
    intids = component.getUtility(IIntIds)
    id = intids.register(value)
    # and index the relation with the catalog
    catalog = component.getUtility(ICatalog)
    catalog.index_doc(id, value)

def _relations(obj):
    """Given an object, return tuples of name, relation value.

    Only real relations are returned, not temporary relations.
    """
    for name, relation in _potential_relations(obj):
        if IRelationValue.providedBy(relation):
            yield name, relation

def _potential_relations(obj):
    """Given an object return tuples of name, relation value.

    Returns both IRelationValue attributes as well as ITemporaryRelationValue
    attributes.
    """
    for iface in providedBy(obj).flattened():
        for name, field in getFields(iface).items():
            if IRelation.providedBy(field):
                relation = getattr(obj, name)
                yield name, relation
