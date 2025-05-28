from rdflib import RDF, RDFS
from rdflib.namespace import OWL

class Ontology:
    def __init__(self, graph, EX):
            self.g = graph
            self.EX = EX
            self._setup_ontology()

    def _setup_ontology(self):
            """Setup the ontology with classes, properties and their relationships"""
            # Define classes
            self.g.add((self.EX.Element, RDF.type, OWL.Class))
            self.g.add((self.EX.TextElement, RDF.type, OWL.Class))
            self.g.add((self.EX.StructuralElement, RDF.type, OWL.Class))
            self.g.add((self.EX.LinkElement, RDF.type, OWL.Class))
            self.g.add((self.EX.FormElement, RDF.type, OWL.Class))
            
            # Define subclass relationships
            self.g.add((self.EX.TextElement, RDFS.subClassOf, self.EX.Element))
            self.g.add((self.EX.StructuralElement, RDFS.subClassOf, self.EX.Element))
            self.g.add((self.EX.LinkElement, RDFS.subClassOf, self.EX.Element))
            self.g.add((self.EX.FormElement, RDFS.subClassOf, self.EX.Element))
            
            # Define properties
            self.g.add((self.EX.hasChild, RDF.type, OWL.TransitiveProperty))
            self.g.add((self.EX.hasSibling, RDF.type, OWL.SymmetricProperty))
            self.g.add((self.EX.isChildOf, RDF.type, OWL.ObjectProperty))
            self.g.add((self.EX.contains, RDF.type, OWL.ObjectProperty))
            self.g.add((self.EX.isContainedIn, RDF.type, OWL.ObjectProperty))
            self.g.add((self.EX.hasText, RDF.type, OWL.DatatypeProperty))
            self.g.add((self.EX.hasTag, RDF.type, OWL.DatatypeProperty))
            self.g.add((self.EX.hasAttribute, RDF.type, OWL.DatatypeProperty))
            self.g.add((self.EX.hasClass, RDF.type, OWL.DatatypeProperty))
            self.g.add((self.EX.hasId, RDF.type, OWL.DatatypeProperty))
            self.g.add((self.EX.hasHref, RDF.type, OWL.DatatypeProperty))
            self.g.add((self.EX.hasValue, RDF.type, OWL.DatatypeProperty))
            
            # Define inverse properties
            self.g.add((self.EX.hasChild, OWL.inverseOf, self.EX.isChildOf))
            self.g.add((self.EX.contains, OWL.inverseOf, self.EX.isContainedIn))
            
            # Define property domains and ranges
            self.g.add((self.EX.hasChild, RDFS.domain, self.EX.Element))
            self.g.add((self.EX.hasChild, RDFS.range, self.EX.Element))
            self.g.add((self.EX.hasSibling, RDFS.domain, self.EX.Element))
            self.g.add((self.EX.hasSibling, RDFS.range, self.EX.Element))