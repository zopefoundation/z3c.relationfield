import grokcore.component as grok
from xml.sax.saxutils import escape

from zope.app.form.interfaces import IInputWidget, IDisplayWidget
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.app.form.browser import TextWidget, DisplayWidget
from zope import component
from zope.component.interfaces import ComponentLookupError
from zope.app.form.browser.widget import renderElement
from zope.traversing.browser import absoluteURL
from z3c.objpath.interfaces import IObjectPath

from z3c.relationfield.schema import IRelation
from z3c.relationfield.interfaces import IRelationInfo

class RelationWidget(grok.MultiAdapter, TextWidget):
    grok.adapts(IRelation, IBrowserRequest)
    grok.provides(IInputWidget)

    def __call__(self):
        result = TextWidget.__call__(self)
        explorer_url = component.getMultiAdapter((self.context.context,
                                                 self.request),
                                                 name="explorerurl")()
        result += renderElement(
            'input', type='button', value='get relation',
            onclick="Z3C.relation.popup(this.previousSibling, '%s')" %
            explorer_url)
        return result
    
    def _toFieldValue(self, input):
        if not input:
            return None
        # convert path to Relation object
        obj = self.resolve(input)
        # XXX if obj is none, cannot create path
        return IRelationInfo(obj).createRelation()

    def _toFormValue(self, value):
        if value is None:
            return ''
        return value.to_path

    def resolve(self, path):
        object_path = component.getUtility(IObjectPath)
        return object_path.resolve(path)


class RelationDisplayWidget(grok.MultiAdapter, DisplayWidget):
    grok.adapts(IRelation, IBrowserRequest)
    grok.provides(IDisplayWidget)

    def __call__(self):
        if self._renderedValueSet():
            value = self._data
        else:
            value = self.context.default
        if value == self.context.missing_value:
            return ""
        to_object = value.to_object
        try:
            to_url = component.getMultiAdapter((to_object, self.request),
                                               name="relationurl")()
        except ComponentLookupError:
            to_url = absoluteURL(to_object, self.request)
        return '<a href="%s">%s</a>' % (
            to_url,
            escape(value.to_path))

