from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS
from rdflib.namespace import OWL, XSD
import networkx as nx
from sentence_transformers import SentenceTransformer, util


class QueryBasedSearch:
        def __init__(self, graph, EX):
                # Initialize RDF graph
                self.g = graph
                self.EX = EX

                # Initialize sentence transformer model for semantic search
                self.model = SentenceTransformer('all-MiniLM-L6-v2')

        def search_query(self, query_str, threshold=0.3):
                """Semantic search in the knowledge graph"""
                query_embedding = self.model.encode(query_str, convert_to_tensor=True)
                results = []

                # Search through text properties
                for node, text in self.g.subject_objects(self.EX.hasText):
                        text_str = str(text)
                        text_embedding = self.model.encode(text_str, convert_to_tensor=True)
                        cosine_score = util.pytorch_cos_sim(query_embedding, text_embedding).item()
                        if cosine_score >= threshold:
                                results.append((node, text_str, cosine_score))

                # Sort results by similarity
                results.sort(key=lambda x: x[2], reverse=True)
                return results

        def sparql_query(self, query):
                """Run a SPARQL query on the knowledge graph"""
                return self.g.query(query)