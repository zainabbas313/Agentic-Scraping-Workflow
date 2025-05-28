from owlrl import DeductiveClosure, RDFS_Semantics

class RDFSreasoner:
        def __init__(self, graph):
                # Initialize RDF graph
                self.g = graph
                                
        def apply_rdfs_reasoning(self):
                """Apply RDFS reasoning to the knowledge graph"""
                print("Applying RDFS reasoning...")
                DeductiveClosure(RDFS_Semantics).expand(self.g)
                print(f"After RDFS reasoning, graph contains {len(self.g)} triples")