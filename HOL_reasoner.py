
class HOL:
    def __init__(self, graph, EX):
        # Initialize RDF graph
        self.g = graph
        self.EX = EX
        
        
    def apply_higher_order_logic(self):
            """
            Simple demonstration of applying higher-order logic rules
            Note: Full HOL reasoning would require a specialized reasoner
            """
            print("Applying simple higher-order logic rules...")
            
            # Example rule: If A contains B and B contains C, then A contains C (transitive consideration)
            new_triples = []
            
            for s, p, o in self.g.triples((None, self.EX.contains, None)):
                for _, _, o2 in self.g.triples((o, self.EX.contains, None)):
                    new_triples.append((s, self.EX.contains, o2))
            
            # Add the new triples to the graph
            for s, p, o in new_triples:
                self.g.add((s, p, o))
            
            print(f"After HOL rules, graph contains {len(self.g)} triples")