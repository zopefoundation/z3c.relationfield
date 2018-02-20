from z3c.relationfield.interfaces import IRelation
from z3c.relationfield.interfaces import IRelationChoice
from z3c.relationfield.interfaces import IRelationList
from zope.interface import implementer
from zope.schema import Choice
from zope.schema import Field
from zope.schema import List


@implementer(IRelation)
class Relation(Field):
    pass


@implementer(IRelationList)
class RelationList(List):

    def __init__(self, value_type=None, unique=False, **kw):
        if value_type is None:
            value_type = Relation()
        super(RelationList, self).__init__(
            value_type=value_type,
            unique=unique,
            **kw
        )


@implementer(IRelationChoice)
class RelationChoice(Choice):
    pass
