import grokcore.component as grok

try:
    from lxml import etree
    from z3c.schema2xml import IXMLGenerator
    XML_GENERATORS = True
except ImportError:
    XML_GENERATORS = False

from z3c.relationfield.relation import TemporaryRelationValue
from z3c.relationfield.interfaces import IRelationList, IRelation
    
if XML_GENERATORS:
    
    class RelationListGenerator(grok.Adapter):
        """Export a relation list to XML.
        """
        grok.context(IRelationList)
        grok.implements(IXMLGenerator)

        def output(self, container, value):
            element = etree.SubElement(container, self.context.__name__)
            field = self.context.value_type
            if value is not None:
                for v in value:
                    IXMLGenerator(field).output(element, v)

        def input(self, element):
            field = self.context.value_type
            return [
                IXMLGenerator(field).input(sub_element)
                for sub_element in element]

    class RelationGenerator(grok.Adapter):
        """Eport a relation to XML.
        """
        grok.context(IRelation)
        grok.implements(IXMLGenerator)

        def output(self, container, value):
            element = etree.SubElement(container, self.context.__name__)
            if value is not None:
                element.text = value.to_path

        def input(self, element):
            if element.text is None:
                return None
            path = element.text
            return TemporaryRelationValue(path)
