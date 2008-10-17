import grokcore.component as grok

from lxml import etree

from zope.interface import implements
from zope.schema import Field

import z3c.schema2xml

from z3c.relationfield.interfaces import IRelation
from z3c.relationfield.relation import TemporaryRelationValue

class Relation(Field):
    implements(IRelation)

class RelationGenerator(grok.Adapter):
    """Eport a relation to XML.
    """
    grok.context(IRelation)
    grok.implements(z3c.schema2xml.IXMLGenerator)

    def output(self, container, value):
        element = etree.SubElement(container, self.context.__name__)
        if value is not None:
            element.text = value.to_path

    def input(self, element):
        if element.text is None:
            return None
        path = element.text
        return TemporaryRelationValue(path)
