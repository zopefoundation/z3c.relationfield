import grok

from lxml import etree

from zope import schema
from zope.interface import implements
from zope.schema.interfaces import IField
from zope.schema import Field

from z3c.objpath.interfaces import IObjectPath
import z3c.schema2xml

from z3c.relationfield.relation import TemporaryRelation

class IRelation(IField):
    pass

class Relation(Field):
    implements(IRelation)

class RelationGenerator(grok.Adapter):
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
        return TemporaryRelation(path)
