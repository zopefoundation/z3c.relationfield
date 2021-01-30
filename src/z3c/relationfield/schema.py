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
    value_in_vocabulary = True

    def __init__(self, **kw):
        if 'value_in_vocabulary' in kw:
            self.value_in_vocabulary = kw.pop('value_in_vocabulary')
        super(RelationChoice, self).__init__(**kw)

    def _validate(self, value):
        if self._init_field:
            return

        # Vocabulary validation expects a vocabulary values to match field
        # values, which isn't always the case when the value could be a
        # relation, an object path, uuid, or the object itself. Optionally skip
        # vocabulary validation, but always call other base class validators.
        if self.value_in_vocabulary:
            super(RelationChoice, self)._validate(value)
        else:
            super(Choice, self)._validate(value)
