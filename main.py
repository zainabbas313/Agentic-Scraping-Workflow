from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS
from rdflib.namespace import OWL, XSD
from owlrl import DeductiveClosure, OWLRL_Semantics, RDFS_Semantics
from bs4 import BeautifulSoup, Tag
import networkx as nx
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer, util
import requests
import os
import re
# from pyvis.network import Network
import uuid

from webpage_fetcher import WebpageFetcher
from ontology_setup import Ontology
from knowledge_graph import KnowledgeGraph
from HOL_reasoner import HOL
from owl_reasoner import OWLreasoner
from rdfs_reasoner import RDFSreasoner
from sparql_query_search import QueryBasedSearch
from ULKB_logic_rules import ULKBrules

class WebAgent:
    def __init__(self, base_namespace="http://example.org/"):
        # Initialize RDF graph
        self.g = Graph()
        self.EX = Namespace(base_namespace)
        self.g.bind("ex", self.EX)
        self.g.bind("owl", OWL)
        self.g.bind("rdfs", RDFS)
        
        self.counter = 1
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def process_webpage(url):
        """Process a webpage and build a knowledge graph"""
        # Initialize the knowledge graph builder
        Agent = WebAgent(url)
        html_extractor = WebpageFetcher()
        Ontology(Agent.g,Agent.EX)
        kg_builder = KnowledgeGraph(Agent.g,Agent.EX)
        
        # Fetch the HTML content
        print(f"Fetching HTML from {url}...")
        html_content = html_extractor.fetch(url)
        
        if not html_content:
            print("Failed to fetch HTML content")
            return
        # print(html_content)
        # Build the knowledge graph
        print("Building knowledge graph...")
        Agent.g = kg_builder.build_knowledge_graph(html_content, url)
        print(f"Initial graph contains {len(Agent.g)} triples")
        
        # Apply reasoning | use any one from these four reasoners
        OWL_reasoner = OWLreasoner(Agent.g)
        OWL_reasoner.apply_owl_reasoning()

        # RDFS_reasoner = RDFSreasoner(Agent.g)
        # RDFS_reasoner.apply_rdfs_reasoning()

        # HOL_reasoner = HOL(Agent.g, Agent.EX)
        # HOL_reasoner.apply_higher_order_logic()

        # ULKB_rules = ULKBrules(Agent.g, Agent.EX)
        # ULKB_rules.apply_universal_logic_knowledge_base()
        
        # calcaltion the centrality
        # nx_graph = kg_builder.compute_centrality()
        
        # for visualization
        # kg_builder.save_graph_visualization(nx_graph, "knowledge_graph_visualization1.html")
        
        # for storing the KG
        # kg_builder.save_to_file("knowledge_graph1.ttl")
        
        print(f"Graph contains {len(Agent.g)} triples")
        print("\nPerforming  semantic search:")
        search = QueryBasedSearch(Agent.g, Agent.EX)
        search_results = search.search_query("product price", threshold=0.3)
        for node, text, score in search_results[:5]:  # Show top 5 results
            print(f"Node: {node}, Text: '{text}', Similarity: {score:.3f}")
        
        print("\nPerforming example SPARQL query:")
        sparql_query = """
        PREFIX ex: <""" + url + """>
        SELECT ?element ?text
        WHERE {
        ?element a ?type .
        ?element ex:hasText ?text .
        FILTER(CONTAINS(LCASE(?text), "price"))
        }
        """
        results = search.sparql_query(sparql_query)
        for row in results:
            print(f"Element: {row.element}, Text: {row.text}\n\n")
        
        print("\nProcessing complete!")


if __name__ == "__main__":
    url_to_process = "https://www.amazon.com/Amazon-Essentials-Mens-Derby-Black/dp/B0BNBS1JRR/ref=sr_1_1_ffob_sspa?dib=eyJ2IjoiMSJ9.C84byVgb2mDkuzXYjKA2jDEoFGJ-3QHatSfYILE8lAuGB5XDkH-wLyb5lRsa2w5djimNlrVbF_0wx27FR1jAS_av-Iil_cVKOFEh4IEwIbjzga9m4dLSC27LHJK_qVafPW3fiKqJkeB7ELZR08ufPhh5WDwAc6j3lO69vJQLKLy8bfj39Be0LDOfRqll2p5wvv6ajDP_PLskKDXucnvQKOLg-1DILu7CYlKnk4au_5k-GkixUXjm4BdTaZHWqPV_1iYo0YjFJ15nppFpuLrSU5vX5kvebVCBQrq9gSpVAQA.Wuv3sEHChnSYqh4iNmHgj_CBs9sG6iXH5oQc5cf6xSU&dib_tag=se&keywords=Shoes&qid=1741447666&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1&psc=1"
    
    # url_to_process = "https://www.amazon.com/Picozon-Magnetic-Organizer-Adhesive-Management/dp/B0CZQ5528D/ref=sr_1_5?adgrpid=175050041160&dib=eyJ2IjoiMSJ9.1VgYjlMxuEvrfZedx-O2jJE5bsK-oc7zMLIzC8j0C-gsXMuZxSh9OQBq7FYHPNqYYtmd1UQgtp3rSv6uV_RXS3W3yTGS-3mbKBg22HT6Rjrmww0sEIVADTCRAQT72teNPBj8XZXAYi2GDcrUEiqrLBlkvV41VRB6joC6ZzoryRe-yCrUxzDK0UWWJRC6kt9t4WvTsdBlZNbtCEOpamclH9dh72cKxEYiFjbzLmhFmcjk6ynSZRUt0gyQualAivsE59-9CPMF_Z6EeFMA5t0VNdUnjCFOc4l8thhnshxBHL8-mMvw2jAKdi_fUMVN_W57pYfDpjThLTQsB1arVf0KacKdoKFQvdYWQNOGWee2JUjMRuGyUfcFvDnXkKLO6T0iH5rhQ2z62Y2Vo7w-lEZ5JIbT79EiMKFj31Je1lJYgdMcczDUS-2gJDRimgtnxwuV._JNnehsKixsBIdZu5uK-Ov0vck1UmgPJlBtbkQtep_A&dib_tag=se&hvadid=726823073705&hvdev=c&hvlocphy=9077136&hvnetw=g&hvqmt=b&hvrand=8615028732654151166&hvtargid=kwd-300129314550&hydadcr=17827_13648628&keywords=amazon%2Busa%2Bshop&mcid=3077e3fdbb5f3d849b7e360021ad7932&qid=1740663058&sr=8-5&th=1"
    
    WebAgent.process_webpage(url_to_process)