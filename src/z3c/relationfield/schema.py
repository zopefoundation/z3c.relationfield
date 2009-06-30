from zope.interface import implements
from zope.schema import Field, List, Choice

from z3c.relationfield.interfaces import IRelation, IRelationChoice, IRelationList

class Relation(Field):
    implements(IRelation)

class RelationList(List):
    implements(IRelationList)

    value_type = Relation()

class RelationChoice(Choice):
    implements(IRelationChoice)