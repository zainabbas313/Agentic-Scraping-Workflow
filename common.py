"""
Module: common.py
Description: Contains common types, exception classes, and helper functions used across the application.
"""

import re
import logging

# Configure a common logger for all modules.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

class InvalidURLException(Exception):
    """
    Raised when the URL provided is not a valid URL.

    Attributes:
        url (str): The invalid URL that caused the exception.
        message (str): Explanation of the error.
    """

    def __init__(self, url: str, message: str = "The provided URL is invalid"):
        """
        Initialize the InvalidURLException.

        Args:
            url (str): The invalid URL.
            message (str, optional): Custom error message. Defaults to "The provided URL is invalid".
        """
        self.url = url
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        """
        String representation of the exception.

        Returns:
            str: Formatted error message.
        """
        return f"{self.message}: {self.url}"


class FetchTimeoutError(Exception):
    """
    Raised when fetching a webpage times out after all retry attempts.

    Attributes:
        url (str): The URL that timed out.
        timeout (int): The timeout duration in seconds.
        message (str): Explanation of the error.
    """

    def __init__(self, url: str, timeout: int, message: str = "Webpage fetch timed out"):
        """
        Initialize the FetchTimeoutError.

        Args:
            url (str): The URL that timed out.
            timeout (int): The timeout duration in seconds.
            message (str, optional): Custom error message. Defaults to "Webpage fetch timed out".
        """
        self.url = url
        self.timeout = timeout
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        """
        String representation of the exception.

        Returns:
            str: Formatted error message.
        """
        return f"{self.message}: {self.url} (Timeout: {self.timeout} seconds)"


class WebpageFetchError(Exception):
    """
    Raised when an error occurs during webpage fetching.

    Attributes:
        url (str): The URL that caused the fetch error.
        message (str): Explanation of the error.
    """

    def __init__(self, url: str, message: str = "An error occurred while fetching the webpage"):
        """
        Initialize the WebpageFetchError.

        Args:
            url (str): The URL that caused the fetch error.
            message (str, optional): Custom error message. Defaults to "An error occurred while fetching the webpage".
        """
        self.url = url
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        """
        String representation of the exception.

        Returns:
            str: Formatted error message.
        """
        return f"{self.message}: {self.url}"


class ClassificationError(Exception):
    """
    Raised when an error occurs during page classification.

    Attributes:
        url (str): The URL that caused the classification error.
        message (str): Explanation of the error.
    """

    def __init__(self, url: str, message: str = "An error occurred during page classification"):
        """
        Initialize the ClassificationError.

        Args:
            url (str): The URL that caused the classification error.
            message (str, optional): Custom error message. Defaults to "An error occurred during page classification".
        """
        self.url = url
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        """
        String representation of the exception.

        Returns:
            str: Formatted error message.
        """
        return f"{self.message}: {self.url}"
    
def validate_url(url: str) -> bool:
    """
    Validate if the provided string is a well-formed URL.

    @Feature End-to-End Processing via Main Entry Point  
    @Scenario Handling an invalid URL format

    :param url: The URL string to validate.
    :return: True if valid, False otherwise.
    """
    url_regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'\S+$', re.IGNORECASE)
    return re.match(url_regex, url) is not None






# import re
# import logging
# import networkx as nx

# # Configure a common logger for all modules.
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# if not logger.handlers:
#     ch = logging.StreamHandler()
#     formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#     ch.setFormatter(formatter)
#     logger.addHandler(ch)

# # Custom exception classes
# class InvalidURLException(Exception):
#     """Raised when the URL provided is not a valid URL."""
#     pass

# class FetchTimeoutError(Exception):
#     """Raised when fetching a webpage times out after all retry attempts."""
#     pass

# class WebpageFetchError(Exception):
#     """Raised when an error occurs during webpage fetching."""
#     pass

# class ClassificationError(Exception):
#     """Raised when an error occurs during page classification."""
#     pass

# # URL Validation function
# def validate_url(url: str) -> bool:
#     """
#     Validate if the provided string is a well-formed URL.
#     :param url: The URL string to validate.
#     :return: True if valid, False otherwise.
#     """
#     url_regex = re.compile(
#         r'^(?:http|ftp)s?://'  # http:// or https://
#         r'\S+$', re.IGNORECASE)
#     return re.match(url_regex, url) is not None

# # Knowledge Graph Implementation
# class KnowledgeGraph:
#     def __init__(self):
#         """Initialize a directed knowledge graph."""
#         self.graph = nx.DiGraph()
#         logger.info("Knowledge Graph initialized.")

#     def add_concept(self, concept: str):
#         """Add a concept (node) to the graph."""
#         self.graph.add_node(concept)
#         logger.info(f"Added concept: {concept}")

#     def add_relation(self, source: str, relation: str, target: str):
#         """Add a relation (edge) between two concepts."""
#         self.graph.add_edge(source, target, relation=relation)
#         logger.info(f"Added relation: {source} -[{relation}]-> {target}")

#     def query(self, concept: str):
#         """Retrieve all concepts directly connected to a given concept."""
#         neighbors = list(self.graph.neighbors(concept))
#         logger.info(f"Queried {concept}: {neighbors}")
#         return neighbors