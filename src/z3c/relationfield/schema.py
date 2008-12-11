import grokcore.component as grok

from lxml import etree

from zope.interface import implements
from zope.schema import Field, List

import z3c.schema2xml

from z3c.relationfield.interfaces import IRelation, IRelationList
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

class RelationList(List):
    implements(IRelationList)

    value_type = Relation()
    
class RelationListGenerator(grok.Adapter):
    """Export a relation list to XML.
    """
    grok.context(IRelationList)
    grok.implements(z3c.schema2xml.IXMLGenerator)

    def output(self, container, value):
        element = etree.SubElement(container, self.context.__name__)
        field = self.context.value_type
        if value is not None:
            for v in value:
                IXMLGenerator(field).output(container, v)

    def input(self, element):
        field = self.context.value_type
        return [
            IXMLGenerator(field).input(sub_element)
            for sub_element in element]

