========
Relation
========

This package implements a new schema field Relation, and the
RelationValue objects that store actual relations. It can index these
relations using the ``zc.relation`` infractructure, and therefore
efficiently answer questions about the relations.

The package `z3c.relationfieldui`_ in addition provides a widget to
edit and display Relation fields.

.. _`z3c.relationfieldui`: http://pypi.python.org/pypi/z3c.relationfieldui

The Relation field
------------------

First, some bookkeeping that can go away as soon as we release a fixed
Grok. We first need to grok ftests to make sure we have the right
utilities registered::

  >>> import grokcore.component as grok
  >>> grok.testing.grok('z3c.relationfield.ftests')

We previously defined an interface ``IItem`` with a relation field in
it. We also defined a class ``Item`` that implements both ``IItem``
and the special ``z3c.relationfield.interfaces.IHasRelations``
interface. The ``IHasRelation`` marker interface is needed to let the
relations be cataloged. Unfortunately we cannot define ``Item`` and
``IItem`` in the doctest here, as these objects need to be stored in
the ZODB cleanly and therefore need to be in a module.  Let's set up a
test application in a container::

  >>> root = getRootFolder()['root'] = TestApp()

We make sure that this is the current site, so we can look up local
utilities in it and so on::

  >>> from zope.app.component.hooks import setSite
  >>> setSite(root)

We'll add an item ``a`` to it::

  >>> root['a'] = Item()

All items, including the one we just created, should have unique int
ids as this is required to link to them::

  >>> from zope import component
  >>> from zope.app.intid.interfaces import IIntIds
  >>> intids = component.getUtility(IIntIds)
  >>> a_id = intids.getId(root['a'])
  >>> a_id >= 0
  True

The relation is currently ``None``::

  >>> root['a'].rel is None
  True

Now we can create an item ``b`` that links to item ``a``::

  >>> from z3c.relationfield import RelationValue
  >>> b = Item()
  >>> b.rel = RelationValue(a_id)

We now store the ``b`` object, which will also set up its relation::

  >>> root['b'] = b

Let's examine the relation. First we'll check which attribute of the
pointing object ('b') this relation is pointing from::

  >>> root['b'].rel.from_attribute
  'rel'

We can ask for the object it is pointing at::

  >>> to_object = root['b'].rel.to_object
  >>> to_object.__name__
  u'a'

We can also get the object that is doing the pointing; since we
supplied the ``IHasRelations`` interface, the event system took care
of setting this::

  >>> from_object = root['b'].rel.from_object
  >>> from_object.__name__
  u'b'
 
This object is also known as the ``__parent__``; again the event
sytem took care of setting this::

  >>> parent_object = root['b'].rel.__parent__
  >>> parent_object is from_object
  True

The relation also knows about the interfaces of both the pointing object
and the object that is being pointed at::

  >>> sorted(root['b'].rel.from_interfaces)
  [<InterfaceClass zope.annotation.interfaces.IAttributeAnnotatable>, 
   <InterfaceClass zope.app.container.interfaces.IContained>,
   <InterfaceClass grokcore.component.interfaces.IContext>,
   <InterfaceClass z3c.relationfield.interfaces.IHasRelations>, 
   <InterfaceClass z3c.relationfield.ftests.IItem>, 
   <InterfaceClass persistent.interfaces.IPersistent>]

  >>> sorted(root['b'].rel.to_interfaces)
  [<InterfaceClass zope.annotation.interfaces.IAttributeAnnotatable>, 
   <InterfaceClass zope.app.container.interfaces.IContained>, 
   <InterfaceClass grokcore.component.interfaces.IContext>,
   <InterfaceClass z3c.relationfield.interfaces.IHasRelations>,
   <InterfaceClass z3c.relationfield.ftests.IItem>, 
   <InterfaceClass persistent.interfaces.IPersistent>]

We can also get the interfaces in flattened form::

  >>> sorted(root['b'].rel.from_interfaces_flattened)
  [<InterfaceClass zope.annotation.interfaces.IAnnotatable>, 
   <InterfaceClass zope.annotation.interfaces.IAttributeAnnotatable>, 
   <InterfaceClass zope.app.container.interfaces.IContained>,
   <InterfaceClass grokcore.component.interfaces.IContext>, 
   <InterfaceClass z3c.relationfield.interfaces.IHasRelations>,   
   <InterfaceClass z3c.relationfield.ftests.IItem>, 
   <InterfaceClass zope.location.interfaces.ILocation>, 
   <InterfaceClass persistent.interfaces.IPersistent>, 
   <InterfaceClass zope.interface.Interface>]
  >>> sorted(root['b'].rel.to_interfaces_flattened)
  [<InterfaceClass zope.annotation.interfaces.IAnnotatable>, 
   <InterfaceClass zope.annotation.interfaces.IAttributeAnnotatable>, 
   <InterfaceClass zope.app.container.interfaces.IContained>,
   <InterfaceClass grokcore.component.interfaces.IContext>,
   <InterfaceClass z3c.relationfield.interfaces.IHasRelations>,
   <InterfaceClass z3c.relationfield.ftests.IItem>, 
   <InterfaceClass zope.location.interfaces.ILocation>, 
   <InterfaceClass persistent.interfaces.IPersistent>, 
   <InterfaceClass zope.interface.Interface>]

Paths
-----

We can also obtain the path of the relation (both from where it is
pointing as well as to where it is pointing). The path should be a
human-readable reference to the object we are pointing at, suitable
for serialization. In order to work with paths, we first need to set
up an ``IObjectPath`` utility.

Since in this example we only place objects into a single flat root
container, the paths in this demonstration can be extremely simple:
just the name of the object we point to. In more sophisticated
applications a path would typically be a slash separated path, like
``/foo/bar``::

  >>> from z3c.objpath.interfaces import IObjectPath
  >>> class ObjectPath(grok.GlobalUtility):
  ...   grok.provides(IObjectPath)
  ...   def path(self, obj):
  ...       return obj.__name__
  ...   def resolve(self, path):
  ...       return root[path]

  >>> grok.testing.grok_component('ObjectPath', ObjectPath)
  True

After this, we can get the path of the object the relation points to::

  >>> root['b'].rel.to_path
  u'a'

We can also get the path of the object that is doing the pointing::

  >>> root['b'].rel.from_path
  u'b'

Relation queries
----------------

Now that we have set up and indexed a relationship between ``a`` and
``b``, we can issue queries using the relation catalog. Let's first
get the catalog::

  >>> from zc.relation.interfaces import ICatalog
  >>> catalog = component.getUtility(ICatalog)

Let's ask the catalog about the relation from ``b`` to ``a``::

  >>> l = sorted(catalog.findRelations({'to_id': intids.getId(root['a'])}))
  >>> l
  [<z3c.relationfield.relation.RelationValue object at ...>]

We look at this relation object again. We indeed go the right one::

  >>> rel = l[0]
  >>> rel.from_object.__name__
  u'b'
  >>> rel.to_object.__name__
  u'a'
  >>> rel.from_path
  u'b'
  >>> rel.to_path
  u'a'

Asking for relations to ``b`` will result in an empty list, as no such
relations have been set up::

  >>> sorted(catalog.findRelations({'to_id': intids.getId(root['b'])}))
  []
 
We can also issue more specific queries, restricting it on the
attribute used for the relation field and the interfaces provided by
the related objects. Here we look for all relations between ``b`` and
``a`` that are stored in object attribute ``rel`` and are pointing
from an object with interface ``IItem`` to another object with the
interface ``IItem``::

  >>> sorted(catalog.findRelations({
  ...   'to_id': intids.getId(root['a']),
  ...   'from_attribute': 'rel',
  ...   'from_interfaces_flattened': IItem,
  ...   'to_interfaces_flattened': IItem}))
  [<z3c.relationfield.relation.RelationValue object at ...>]

There are no relations stored for another attribute::

  >>> sorted(catalog.findRelations({
  ...   'to_id': intids.getId(root['a']),
  ...   'from_attribute': 'foo'}))
  []

There are also no relations stored for a new interface we'll introduce
here::

  >>> class IFoo(IItem):
  ...   pass

  >>> sorted(catalog.findRelations({
  ...   'to_id': intids.getId(root['a']),
  ...   'from_interfaces_flattened': IItem,
  ...   'to_interfaces_flattened': IFoo}))
  []

Changing the relation
---------------------

Let's create a new object ``c``::

  >>> root['c'] = Item()
  >>> c_id = intids.getId(root['c'])

Nothing points to ``c`` yet::

  >>> sorted(catalog.findRelations({'to_id': c_id})) 
  []

We currently have a relation from ``b`` to ``a``::

  >>> sorted(catalog.findRelations({'to_id': intids.getId(root['a'])})) 
  [<z3c.relationfield.relation.RelationValue object at ...>]

We can change the relation to point at a new object ``c``::

  >>> root['b'].rel = RelationValue(c_id)

We need to send an ``IObjectModifiedEvent`` to let the catalog know we
have changed the relations::

  >>> from zope.event import notify
  >>> from zope.lifecycleevent import ObjectModifiedEvent
  >>> notify(ObjectModifiedEvent(root['b']))

We should find now a single relation from ``b`` to ``c``::

  >>> sorted(catalog.findRelations({'to_id': c_id})) 
  [<z3c.relationfield.relation.RelationValue object at ...>]

The relation to ``a`` should now be gone::

  >>> sorted(catalog.findRelations({'to_id': intids.getId(root['a'])})) 
  []

Removing the relation
---------------------

We have a relation from ``b`` to ``c`` right now::

  >>> sorted(catalog.findRelations({'to_id': c_id})) 
  [<z3c.relationfield.relation.RelationValue object at ...>]

We can clean up an existing relation from ``b`` to ``c`` by setting it
to ``None``::

  >>> root['b'].rel = None

We need to send an ``IObjectModifiedEvent`` to let the catalog know we
have changed the relations::

  >>> notify(ObjectModifiedEvent(root['b']))

Setting the relation on ``b`` to ``None`` should remove that relation
from the relation catalog, so we shouldn't be able to find it anymore::

  >>> sorted(catalog.findRelations({'to_id': intids.getId(root['c'])})) 
  []

Let's reestablish the removed relation::

  >>> root['b'].rel = RelationValue(c_id)
  >>> notify(ObjectModifiedEvent(root['b']))

  >>> sorted(catalog.findRelations({'to_id': c_id})) 
  [<z3c.relationfield.relation.RelationValue object at ...>]
          
Copying an object with relations
--------------------------------

Let's copy an object with relations::

  >>> from zope.copypastemove.interfaces import IObjectCopier
  >>> IObjectCopier(root['b']).copyTo(root)
  u'b-2'
  >>> u'b-2' in root
  True

Two relations to ``c`` can now be found, one from the original, and
the other from the copy::

  >>> l = sorted(catalog.findRelations({'to_id': c_id})) 
  >>> len(l)
  2
  >>> l[0].from_path
  u'b'
  >>> l[1].from_path
  u'b-2'

Removing an object with relations
---------------------------------

We will remove ``b-2`` again. Its relation should automatically be removed
from the catalog::

  >>> del root['b-2']
  >>> l = sorted(catalog.findRelations({'to_id': c_id}))
  >>> len(l)
  1
  >>> l[0].from_path
  u'b'

Temporary relations
-------------------

If we have an import procedure where we import relations from some
external source such as an XML file, it may be that we read a relation
that points to an object that does not yet exist as it is yet to be
imported. We provide a special ``TemporaryRelationValue`` for this
case.  A ``TemporaryRelationValue`` just contains the path of what it
is pointing to, but does not resolve it yet. Let's use
``TemporaryRelationValue`` in a new object, creating a relation to
``a``::

  >>> from z3c.relationfield import TemporaryRelationValue
  >>> root['d'] = Item()
  >>> root['d'].rel = TemporaryRelationValue('a')

A modification event does not actually get this relation cataloged::

  >>> before = sorted(catalog.findRelations({'to_id': a_id}))
  >>> notify(ObjectModifiedEvent(root['d']))
  >>> after = sorted(catalog.findRelations({'to_id': a_id}))
  >>> len(before) == len(after)
  True

We will now convert all temporary relations on ``d`` to real ones::

  >>> from z3c.relationfield import realize_relations
  >>> realize_relations(root['d'])
  >>> notify(ObjectModifiedEvent(root['d']))

The relation will now show up in the catalog::

  >>> after2 = sorted(catalog.findRelations({'to_id': a_id}))
  >>> len(after2) > len(before)
  True
