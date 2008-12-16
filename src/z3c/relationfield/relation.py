import grokcore.component as grok

from persistent import Persistent
from zope.interface import implements, providedBy, Declaration
from zope import component
from zope.app.intid.interfaces import IIntIds

from z3c.objpath.interfaces import IObjectPath

from z3c.relationfield.interfaces import (IRelationValue,
                                          ITemporaryRelationValue)

class RelationValue(Persistent):
    implements(IRelationValue)

    def __init__(self, to_id):
        self.to_id = to_id
        # these will be set automatically by RelationProperty
        self.from_object = None
        self.__parent__ = None
        self.from_attribute = None

    @property
    def from_id(self):
        intids = component.getUtility(IIntIds)
        return intids.getId(self.from_object)

    @property
    def from_path(self):
        return _path(self.from_object)

    @property
    def from_interfaces(self):
        return providedBy(self.from_object)

    @property
    def from_interfaces_flattened(self):
        return _interfaces_flattened(self.from_interfaces)
        
    @property
    def to_object(self):
        return _object(self.to_id)

    @property
    def to_path(self):
        return _path(self.to_object)

    @property
    def to_interfaces(self):
        return providedBy(self.to_object)

    @property
    def to_interfaces_flattened(self):
        return _interfaces_flattened(self.to_interfaces)

    def __cmp__(self, other):
        if other is None:
            return cmp(self.to_id, None)
        return cmp(self.to_id, other.to_id)

class TemporaryRelationValue(Persistent):
    """A relation that isn't fully formed yet.

    It needs to be finalized afterwards, when we are sure all potential
    target objects exist.
    """
    grok.implements(ITemporaryRelationValue)
    
    def __init__(self, to_path):
        self.to_path = to_path

    def convert(self):
        object_path = component.getUtility(IObjectPath)
        # XXX what if we have a broken relation?
        to_object = object_path.resolve(self.to_path)
        intids = component.getUtility(IIntIds)
        to_id = intids.getId(to_object)
        return RelationValue(to_id)
    
def _object(id):
    intids = component.getUtility(IIntIds)
    try:
        return intids.getObject(id)
    except KeyError:
        # XXX catching this error is not the right thing to do.
        # instead, breaking a relation by removing an object should
        # be caught and the relation should be adjusted that way.
        return None

def _path(obj):
    if obj is None:
        return ''
    object_path = component.getUtility(IObjectPath)
    return object_path.path(obj)

def _interfaces_flattened(interfaces):
    return Declaration(*interfaces).flattened()

def create_relation(obj):
    intids = component.getUtility(IIntIds)
    return RelationValue(intids.getId(obj))
