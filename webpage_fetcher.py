"""
Module: webpage_fetcher.py
Description: Implements the WebpageFetcher class responsible for dynamically fetching and rendering webpages using Playwright.
"""

import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from common import validate_url, InvalidURLException, FetchTimeoutError, WebpageFetchError, logger

class WebpageFetcher:
    """
    Class for fetching a fully rendered webpage using Playwright.

    @Feature Dynamic Webpage Fetching and Rendering  
    @Scenario Successfully fetching a webpage with dynamic JavaScript content  
    @Scenario Applying exponential backoff on fetch timeouts  
    @Scenario Handling network or unreachable URL errors
    """
    
    def __init__(self):
        # Initialize any configuration or state if needed.
        pass
    
    def fetch(self, url: str, timeout: int = 30, retries: int = 3, delay: int = 2) -> str:
        """
        Fetch the webpage content with DOM cleaning using Playwright.

        :param url: URL of the webpage to fetch.
        :param timeout: Timeout in seconds for each fetch attempt.
        :param retries: Number of retry attempts.
        :param delay: Initial delay (in seconds) between retries.
        :return: Clean HTML content with text-only focus as a string.
        :raises InvalidURLException: If the URL is invalid.
        :raises FetchTimeoutError: If all retry attempts fail.
        :raises WebpageFetchError: For other fetch errors.
        """
        if not isinstance(url, str) or not validate_url(url):
            logger.error(f"Invalid URL provided: {url}")
            raise InvalidURLException(f"Invalid URL: {url}")

        for attempt in range(retries):
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    page.goto(url, timeout=timeout * 1000)
                    page.wait_for_load_state("load", timeout=timeout * 1000)

                    # Clean up DOM before extracting content
                    page.evaluate("""() => {
                        // Remove script-related elements
                        document.querySelectorAll('script, noscript').forEach(e => e.remove());
                        
                        // Remove style-related elements
                        document.querySelectorAll('style, link[rel="stylesheet"]').forEach(e => e.remove());
                        
                        // Remove images and visual media
                        document.querySelectorAll('img, picture, figure, svg, canvas').forEach(e => e.remove());
                        
                        // Remove links while preserving text
                        document.querySelectorAll('a').forEach(a => {
                            const parent = a.parentNode;
                            while (a.firstChild) {
                                parent.insertBefore(a.firstChild, a);
                            }
                            parent.removeChild(a);
                        });
                        
                        // Remove HTML comments
                        const commentWalker = document.createTreeWalker(
                            document,
                            NodeFilter.SHOW_COMMENT
                        );
                        let commentNode;
                        while ((commentNode = commentWalker.nextNode())) {
                            commentNode.parentNode.removeChild(commentNode);
                        }
                    }""")

                    html = page.content()
                    browser.close()
                    logger.info(f"Cleaned webpage fetched on attempt {attempt+1} for URL: {url}")
                    return html
            except PlaywrightTimeoutError as te:
                logger.warning(f"Timeout on attempt {attempt+1} for URL {url}: {te}")
            except Exception as e:
                logger.error(f"Error fetching URL {url} on attempt {attempt+1}: {e}")
            time.sleep(delay * (2 ** attempt))
        logger.error(f"Failed to fetch webpage after {retries} attempts for URL: {url}")
        raise FetchTimeoutError(f"Failed to fetch webpage: {url}")

