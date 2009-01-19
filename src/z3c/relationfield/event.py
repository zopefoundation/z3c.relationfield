import grokcore.component as grok

from zope.interface import providedBy
from zope.schema import getFields
from zope import component
from zope.app.intid.interfaces import IIntIds, IIntIdRemovedEvent
from zope.app.container.interfaces import (IObjectAddedEvent,
                                           IObjectRemovedEvent)
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from zc.relation.interfaces import ICatalog

from z3c.relationfield.interfaces import (IHasOutgoingRelations,
                                          IHasIncomingRelations,
                                          IRelation, IRelationList,
                                          IRelationValue,
                                          ITemporaryRelationValue)

@grok.subscribe(IHasOutgoingRelations, IObjectAddedEvent)
def addRelations(obj, event):
    """Register relations.

    Any relation object on the object will be added.
    """
    for name, relation in _relations(obj):
         _setRelation(obj, name, relation)

@grok.subscribe(IHasOutgoingRelations, IObjectRemovedEvent)
def removeRelations(obj, event):
    """Remove relations.

    Any relation object on the object will be removed from the catalog.
    """
    catalog = component.getUtility(ICatalog)
 
    for name, relation in _relations(obj):
        if relation is not None:
            catalog.unindex(relation)

@grok.subscribe(IHasOutgoingRelations, IObjectModifiedEvent)
def updateRelations(obj, event):
    """Re-register relations, after they have been changed.
    """
    catalog = component.getUtility(ICatalog)
    intids = component.getUtility(IIntIds)

    # remove previous relations coming from id (now have been overwritten)
    # have to activate query here with list() before unindexing them so we don't
    # get errors involving buckets changing size
    rels = list(catalog.findRelations({'from_id': intids.getId(obj)}))
    for rel in rels:
        catalog.unindex(rel)    

    # add new relations
    addRelations(obj, event)

@grok.subscribe(IIntIdRemovedEvent)
def breakRelations(event):
    """Break relations on any object pointing to us.

    That is, store the object path on the broken relation.
    """
    obj = event.object
    if not IHasIncomingRelations.providedBy(obj):
        return
    catalog = component.getUtility(ICatalog)
    intids = component.getUtility(IIntIds)

    # find all relations that point to us
    rels = list(catalog.findRelations({'to_id': intids.getId(obj)}))
    for rel in rels:
        rel.broken(rel.to_path)
    
def realize_relations(obj):
    """Given an object, convert any temporary relations on it to real ones.
    """
    for name, index, relation in _potential_relations(obj):
        if ITemporaryRelationValue.providedBy(relation):
            if index is None:
                # relation
                setattr(obj, name, relation.convert())
            else:
                # relation list
                getattr(obj, name)[index] = relation.convert()

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
    for name, index, relation in _potential_relations(obj):
        if IRelationValue.providedBy(relation):
            yield name, relation

def _potential_relations(obj):
    """Given an object return tuples of name, index, relation value.

    Returns both IRelationValue attributes as well as ITemporaryRelationValue
    attributes.

    If this is a IRelationList attribute, index will contain the index
    in the list. If it's a IRelation attribute, index will be None.
    """
    for iface in providedBy(obj).flattened():
        for name, field in getFields(iface).items():
            if IRelation.providedBy(field):
                try:
                    relation = getattr(obj, name)
                except AttributeError:
                    # can't find this relation on the object
                    continue
                yield name, None, relation
            if IRelationList.providedBy(field):
                try:
                    l = getattr(obj, name)
                except AttributeError:
                    # can't find the relation list on this object
                    continue
                if l is not None:
                    for i, relation in enumerate(l):
                        yield name, i, relation
