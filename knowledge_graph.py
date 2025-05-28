from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS
from rdflib.namespace import OWL, XSD
from bs4 import BeautifulSoup
import uuid
import networkx as nx

class KnowledgeGraph:
    def __init__(self, graph, namespace):
            # Initialize RDF graph
            self.g = graph
            self.EX = Namespace(namespace)
            
            
            # Set up namespaces
            self.counter = 1

    def _determine_element_type(self, element):
        """Determine the type of HTML element based on its tag and attributes"""
        tag = element.name
        
        # Text elements
        if tag in ['p', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 'blockquote', 'pre', 'code']:
            return self.EX.TextElement
        
        # Link elements
        elif tag in ['a', 'link', 'button']:
            return self.EX.LinkElement
        
        # Form elements
        elif tag in ['form', 'input', 'select', 'textarea', 'button', 'label', 'option']:
            return self.EX.FormElement
        
        # Structural elements
        elif tag in ['div', 'section', 'article', 'aside', 'header', 'footer', 'nav', 'main', 'ul', 'ol', 'li', 'table', 'tr', 'td', 'th']:
            return self.EX.StructuralElement
        
        # Default
        return self.EX.Element
    
    def _generate_uri_for_element(self, element):
        """Generate a unique URI for an HTML element"""
        self.counter += 1
        
        # Try to use ID if available
        if element.get('id'):
            return self.EX[f"{element.name}_{element.get('id')}"]
        
        # Or use a unique counter
        return self.EX[f"element_{self.counter}_{element.name}"]
    
    def build_knowledge_graph(self, html_content, url=None):
        """Build a knowledge graph from HTML content with text relationships"""
        if not html_content:
            return None
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Add page metadata
        page_uri = self._add_page_metadata(soup, url)
        
        # Process HTML structure recursively
        if soup.html:
            self._process_element(soup.html, parent_uri=page_uri)
            
        return self.g

    def _add_page_metadata(self, soup, url):
        """Add page metadata to the graph"""
        # Create URI using the EX namespace - this was the error
        page_id = URIRef(f"{self.EX}page_{uuid.uuid4()}")
        
        # Add basic page info
        self.g.add((page_id, RDF.type, self.EX.WebPage))
        
        # Add URL if available
        if url:
            self.g.add((page_id, self.EX.url, Literal(url)))
        
        # Add page title if available
        title_tag = soup.find('title')
        if title_tag:
            self.g.add((page_id, self.EX.title, Literal(title_tag.string)))
        
        return page_id

    def _add_element_node(self, element, parent_uri, sibling_uri):
        """Create a node with HTML element metadata"""
        # Fixed URI creation
        node_id = URIRef(f"{self.EX}node_{uuid.uuid4()}")
        
        # Extract cleaned text content (direct text only)
        direct_text = ' '.join(
            string.strip() 
            for string in element.stripped_strings
            if string.parent == element
        )
        
        # Node properties
        self.g.add((node_id, self.EX.tagName, Literal(element.name)))
        self.g.add((node_id, self.EX.directText, Literal(direct_text)))
        self.g.add((node_id, self.EX.fullText, Literal(element.get_text(" ", strip=True))))
        
        # Structural relationships
        if parent_uri:
            self._add_structural_relationship(node_id, parent_uri, "hasParent")
        if sibling_uri:
            self._add_structural_relationship(node_id, sibling_uri, "siblingOf")
            
        return node_id

    def _store_text_content(self, element, node_uri):
        """Store text relationships with semantic annotations"""
        # Add text content with context
        text_content = element.get_text(" ", strip=True)
        if text_content:
            # Fixed URI creation
            text_node = URIRef(f"{self.EX}text_{uuid.uuid4()}")
            self.g.add((text_node, RDF.type, self.EX.TextContent))
            self.g.add((text_node, self.EX.rawText, Literal(text_content)))
            self.g.add((node_uri, self.EX.hasTextContent, text_node))
            
            # Add semantic text chunks
            for idx, sentence in enumerate(sent_tokenize(text_content)):
                # Fixed URI creation
                sentence_node = URIRef(f"{self.EX}sentence_{uuid.uuid4()}")
                self.g.add((sentence_node, RDF.type, self.EX.TextSegment))
                self.g.add((sentence_node, self.EX.textPosition, Literal(idx)))
                self.g.add((sentence_node, self.EX.content, Literal(sentence)))
                self.g.add((text_node, self.EX.hasSegment, sentence_node))

    def _add_structural_relationship(self, source, target, relation):
        """Add hierarchical relationship with OWL properties"""
        self.g.add((source, self.EX[relation], target))
        # Add inverse relationship for parent/child
        if relation == "hasParent":
            self.g.add((target, self.EX.hasChild, source))
        # Add symmetric property for siblings
        if relation == "siblingOf":
            self.g.add((target, self.EX.siblingOf, source))
    
    def _process_element(self, element, parent_uri):
        """Recursively process HTML elements and add them to the graph"""
        # Skip comment nodes
        if element.name is None:
            return None
        
        # Generate URI for this element
        element_uri = self._generate_uri_for_element(element)
        
        # Add element type
        element_type = self._determine_element_type(element)
        self.g.add((element_uri, RDF.type, element_type))
        
        # Add tag name
        self.g.add((element_uri, self.EX.hasTag, Literal(element.name)))
        
        # Add text content if available and not empty
        if element.string and element.string.strip():
            self.g.add((element_uri, self.EX.hasText, Literal(element.string.strip())))
        
        # Add attributes
        for attr, value in element.attrs.items():
            if attr == 'class':
                if isinstance(value, list):
                    for cls in value:
                        self.g.add((element_uri, self.EX.hasClass, Literal(cls)))
                else:
                    self.g.add((element_uri, self.EX.hasClass, Literal(value)))
            elif attr == 'id':
                self.g.add((element_uri, self.EX.hasId, Literal(value)))
            elif attr == 'href':
                self.g.add((element_uri, self.EX.hasHref, Literal(value)))
            elif attr == 'value':
                self.g.add((element_uri, self.EX.hasValue, Literal(value)))
            else:
                self.g.add((element_uri, self.EX.hasAttribute, Literal(f"{attr}:{value}")))
        
        # Add parent-child relationship
        if parent_uri is not None:
            self.g.add((parent_uri, self.EX.hasChild, element_uri))
            self.g.add((element_uri, self.EX.isChildOf, parent_uri))
            
            # Add containment relationship
            self.g.add((parent_uri, self.EX.contains, element_uri))
            self.g.add((element_uri, self.EX.isContainedIn, parent_uri))
        
        # Process child elements
        child_uris = []
        for child in element.find_all(recursive=False):
            if child.name is not None:
                child_uri = self._process_element(child, element_uri)
                if child_uri:
                    child_uris.append(child_uri)
        
        # Add sibling relationships
        for i, uri1 in enumerate(child_uris):
            for uri2 in child_uris[i+1:]:
                self.g.add((uri1, self.EX.hasSibling, uri2))
                # No need to add the symmetric relation as it's defined as symmetric
        
        return element_uri
    
    def compute_centrality(self):
        """Compute centrality measures and add them to the graph"""
        print("Computing centrality measures...")
        
        # Convert RDF graph to NetworkX graph
        nx_graph = nx.Graph()
        for s, p, o in self.g:
            if isinstance(s, URIRef) and isinstance(o, URIRef):
                nx_graph.add_edge(s, o, type=p)
        
        # Compute various centrality measures
        degree_centrality = nx.degree_centrality(nx_graph)
        betweenness_centrality = nx.betweenness_centrality(nx_graph)
        # print(f"The Degree of centrality of the Graph is : {degree_centrality}")
        # print(f"The betweenness centrality of the Graph is : {betweenness_centrality}")
        pagerank = nx.pagerank(nx_graph)
        
        # Add centrality scores to the graph
        for node, score in degree_centrality.items():
            self.g.add((node, self.EX.hasCentralityScore, Literal(score, datatype=XSD.float)))
        
        for node, score in betweenness_centrality.items():
            self.g.add((node, self.EX.hasBetweennessCentrality, Literal(score, datatype=XSD.float)))
        
        for node, score in pagerank.items():
            self.g.add((node, self.EX.hasPageRank, Literal(score, datatype=XSD.float)))
        
        return nx_graph