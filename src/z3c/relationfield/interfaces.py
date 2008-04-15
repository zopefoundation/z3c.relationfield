from zope.interface import Interface, Attribute

class IRelation(Interface):
    from_object = Attribute("The object this relation is pointing from.")

    from_id = Attribute("Id of the object this relation is pointing from.")
    
    from_path = Attribute("The path of the from object.")

    from_interfaces = Attribute("The interfaces of the from object.")

    from_interfaces_flattened = Attribute(
        "Interfaces of the from object, flattened. "
        "This includes all base interfaces.")
    
    from_attribute = Attribute("The name of the attribute of the from object.")
    
    to_object = Attribute("The object this relation is pointing to.")

    to_id = Attribute("Id of the object this relation is pointing to.")

    to_path = Attribute("The path of the object this relation is pointing to.")

    to_interfaces = Attribute("The interfaces of the to-object.")

    to_interfaces_flattened = Attribute(
        "The interfaces of the to object, flattened. "
        "This includes all base interfaces.")

class ITemporaryRelation(Interface):
    """A temporary relation.

    When importing relations from XML, we cannot resolve them into
    true Relation objects yet, as it may be that the object that is
    being related to has not yet been loaded. Instead we create
    a TemporaryRelation object that can be converted into a real one
    after the import has been concluded.
    """
    def convert():
        """Convert temporary relation into a real one.

        Returns real relation object
        """

class IHasRelations(Interface):
    """Marker interface indicating that the object has relations.

    Use this interface to make sure that the relations get added and
    removed from the catalog when appropriate.
    """

class IRelationInfo(Interface):
    """Relationship information for an object.
    """

    def createRelation():
        """Create a relation object pointing to this object.

        Returns an object that provides IRelation.
        """
