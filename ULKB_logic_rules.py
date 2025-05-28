class ULKBrules:
    def __init__(self, graph, EX):
        self.g = graph
        self.EX = EX
       
        
    def apply_universal_logic_knowledge_base(self):
            """
            Demonstration of applying ULKB-like logic rules
            Note: This is a simplification of what a real ULKB would do
            """
            print("Applying ULKB-like rules...")
            
            # Rule: Elements with similar classes might represent similar concepts
            class_elements = {}
            
            # Group elements by class
            for s, _, o in self.g.triples((None, self.EX.hasClass, None)):
                cls = str(o)
                if cls not in class_elements:
                    class_elements[cls] = []
                class_elements[cls].append(s)
            
            # Add semantic similarity relationships for elements with the same class
            for cls, elements in class_elements.items():
                if len(elements) > 1:
                    for i, elem1 in enumerate(elements):
                        for elem2 in elements[i+1:]:
                            self.g.add((elem1, self.EX.hasSimilarPurposeTo, elem2))
                            self.g.add((elem2, self.EX.hasSimilarPurposeTo, elem1))
            
            print(f"After ULKB rules, graph contains {len(self.g)} triples")