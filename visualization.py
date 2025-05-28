from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS
from rdflib.namespace import OWL, XSD
import networkx as nx
from nltk.tokenize import sent_tokenize
from pyvis.network import Network

 
# this class is olny use for make the KG to visualize it
class VisualizationKG:
    def __init__(self, base_namespace="http://example.org/"):
        # Initialize RDF graph
        self.g = Graph()
        self.EX = Namespace(base_namespace)
        self.g.bind("ex", self.EX)
        self.g.bind("owl", OWL)
        self.g.bind("rdfs", RDFS)
        

    def save_graph_visualization(self, nx_graph=None, filename="knowledge_graph.html"):
            """Save an interactive visualization of the graph"""
            if nx_graph is None:
                nx_graph = nx.Graph()
                for s, p, o in self.g:
                    if isinstance(s, URIRef) and isinstance(o, URIRef):
                        nx_graph.add_edge(s, o, type=str(p))
            
            # Create a pyvis network
            net = Network(height="800px", width="100%", notebook=False, directed=True)
            
            # Add nodes
            for node in nx_graph.nodes():
                node_type = None
                for _, p, o in self.g.triples((node, RDF.type, None)):
                    node_type = o
                    break
                
                node_label = str(node).split('/')[-1]
                node_color = "#9CBABA"  # Default color
                
                # Color nodes by type
                if node_type:
                    if node_type == self.EX.TextElement:
                        node_color = "#6BAED6"
                    elif node_type == self.EX.StructuralElement:
                        node_color = "#FD8D3C"
                    elif node_type == self.EX.LinkElement:
                        node_color = "#74C476"
                    elif node_type == self.EX.FormElement:
                        node_color = "#9E9AC8"
                
                # Get tag if available
                tag = None
                for _, _, o in self.g.triples((node, self.EX.hasTag, None)):
                    tag = str(o)
                    break
                
                # Format label with tag if available
                if tag:
                    node_label = f"{tag}: {node_label}"
                
                net.add_node(str(node), label=node_label, title=str(node), color=node_color)
            
            # Add edges
            for source, target, data in nx_graph.edges(data=True):
                edge_type = data.get('type', '')
                if 'hasChild' in str(edge_type):
                    color = "blue"
                elif 'hasSibling' in str(edge_type):
                    color = "green"
                elif 'contains' in str(edge_type):
                    color = "red"
                else:
                    color = "gray"
                
                net.add_edge(str(source), str(target), title=str(edge_type), color=color)
            
            # Set physics options for better visualization
            net.set_options("""
            {
                "physics": {
                    "barnesHut": {
                        "gravitationalConstant": -2000,
                        "centralGravity": 0.1,
                        "springLength": 150,
                        "springConstant": 0.05,
                        "damping": 0.09
                    },
                    "maxVelocity": 50,
                    "minVelocity": 0.1,
                    "timestep": 0.5
                },
                "interaction": {
                    "navigationButtons": true,
                    "keyboard": true,
                    "hover": true
                }
            }
            """)
            
            # Save to HTML file
            net.save_graph(filename)
            print(f"Graph visualization saved to {filename}")
        
    def save_to_file(self, filename="knowledge_graph.ttl", format="turtle"):
            """Save the RDF graph to a file"""
            self.g.serialize(destination=filename, format=format)
            print(f"Knowledge graph saved to {filename}")
