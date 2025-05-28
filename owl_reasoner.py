from rdflib.namespace import OWL
from owlrl import DeductiveClosure, OWLRL_Semantics

class OWLreasoner:
        def __init__(self, graph):
                # Initialize RDF graph
                self.g = graph

        def apply_owl_reasoning(self):
                """Apply OWL-RL reasoning to the knowledge graph"""
                print("Applying OWL-RL reasoning...")
                DeductiveClosure(OWLRL_Semantics).expand(self.g)
                print(f"After OWL-RL reasoning, graph contains {len(self.g)} triples")