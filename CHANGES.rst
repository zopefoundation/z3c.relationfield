CHANGES
*******

1.0 (2023-02-22)
================

Breaking changes:

- Drop support for Python 2.7, 3.5, 3.6.

New features:

- Add support for Python 3.7, 3.8, 3.9, 3.10, 3.11.


0.9.0 (2019-09-15)
==================

New features:

- Provide IRelationBrokenEvent to be able to distinguish the event when
  subscribing to IObjectModifiedEvent
  [vangheem]


0.8.0 (2019-02-13)
==================

New features:

- Adresses `Still uses BTrees wrongly, screws up people changing Interfaces <https://github.com/zopefoundation/z3c.relationfield/issues/4>`_, allows third party software to define which indexes are used.
  [jensens]

Bug fixes:

- Fix DeprecationWarnings in ``tests.py``.
  [jensens]


0.7.1 (2018-11-08)
==================

- Python 3 compatibility: use the implementer decorator and fix ordering
  [ale-rt]

- Python 3 compatibility: Make ``RelationValue`` hashable. [sallner]

- Renamed ``README.txt``to ``README.rst`` and ``CHANGES.txt`` to
  ``CHANGES.rst``.
  [thet]

- Update buildout / travis config
  [tomgross]

- Fix issue where relations are cleared on modify if they are not stored as
  an class attribute. Usecase see https://github.com/plone/Products.CMFPlone/issues/2384
  [tomgross]

0.7 (2015-03-13)
================

- Remove dependencies on zope.app.*
  [davisagli]


0.6.3 (2014-04-15)
==================

* Remove dependency on grok.
  [pbauer, jensens]


0.6.2 (2012-12-06)
==================

* Updated test setup and test to run with current versions of dependent
  packages, thus running with Python 2.6, too.

* Added missing (test) dependencies.

* Rename __neq__ method to __ne__ since __neq__ is not the right builtin
  name for != handlers.


0.6.1 (2009-10-11)
==================

* Fixes broken release.

0.6 (2009-10-11)
================

* Ensure that the value_type of a RelationList is not overwritten to be 'None'
  when the field is constructed.

0.5 (2009-06-30)
================

* Move lxml and schema2xml dependencies to an [xml] extra so that people can
  use this package without having to install lxml, which still causes issues
  on some platforms. If z3c.schema2xml and lxml are not importable, the
  relevant adapters will not be defined, but everything else will still work.

* Subscribe to IIntIdAddedEvent instead of IObjectAddedEvent to prevent
  errors due to subscriber ordering.


0.4.3 (2009-06-04)
==================

* Add missing dependency for lxml.


0.4.2 (2009-04-22)
==================

* Prevent the event failures from failing when utilities are missing or when
  objects do not implement IContained.


0.4.1 (2009-02-12)
==================

* Don't handle ``IObjectModified`` events for objects that do not yet
  have a parent. There is no need to do so anyway, as these objects cannot
  have outgoing relations indexed.

0.4 (2009-02-10)
================

* Introduce a ``RelationChoice`` field that behaves like
  ``schema.Choice`` but tracks relations. In combination with a source
  (such as created by ``RelationSourceFactory`` provided by
  ``z3c.relationfieldui``) this can be used to create drop-down
  selections for relations.

* Clarify the way comparing and sorting of ``RelationValue`` objects is
  done in order to better support choice support.

0.3.2 (2009-01-21)
==================

* When a relation is broken, properly re-catalog things.

0.3.1 (2009-01-20)
==================

* Introduce sensible sort order for relations, based on a
  ``(from_attribute, from_path, to_path)`` tuple.

* Relations will now never compare to ``None``.

0.3 (2009-01-19)
================

* Introduce two new interfaces: ``IHasOutgoingRelations`` and
  ``IHasIncomingRelations``. ``IHasOutgoingRelations`` should be provided
  by objects that actually have relations set on them, so that
  they can be properly cataloged. ``IHasIncomingRelations`` should be
  set on objects that can be related to, so that broken relations
  can be properly tracked. ``IHasRelations`` now extends both,
  so if you provide those on your object you have an object that can
  have both outgoing as well as incoming relations.

* Improve broken relations support. When you now break a relation (by
  removing the relation target), ``to_id`` and ``to_object`` become
  ``None``. ``to_path`` however will remain the path that the relation
  last pointed to. ``TemporaryRelation`` objects that when realized
  are broken relations can also be created.

  You can also for broken status by calling ``isBroken`` on a
  relation.

* The signature of the top-level function ``create_relation``
  changed. It used to take the object to which the relation was to be
  created, but should now get the path (in ``IObjectPath`` terms).
  ``create_relation`` will now create a broken relation object if the
  path cannot be resolved.

0.2 (2009-01-08)
================

* Added support for ``RelationList`` fields. This allows one to
  maintain a list of ``RelationValue`` objects that will be cataloged
  like the regular ``Relation`` fields.

* Get rid of ``IRelationInfo`` adapter requirement. Just define a
  ``create_relation`` function that does the same work.

* When looking for relations on an object be more tolerant if those
  cannot be found (just skip them) - this can happen when a schema is
  changed.

0.1 (2008-12-05)
================

* Initial public release.
