"""Web scraping utilities"""

import asyncio
import logging
import re
from typing import List
from urllib.parse import urlparse
from firecrawl import AsyncFirecrawl
from langchain.chat_models.base import BaseChatModel

from ..config.prompts import PROMPT_CLEAN_MARKDOWN
from ..config.settings import settings
from ..utils.llm_utils import get_chat_model

logger = logging.getLogger(__name__)

#cache setting for faster scraping
#maxAge values in ms:
# 5 minutes: 300000, 1 hour: 3600000, 1 day: 86400000, 1 week: 604800000
MAX_AGE_ONE_WEEK = 604800000  # 1 week in milliseconds for 500% faster scraping

def slugify(text: str, max_length: int = 60) -> str:
    """
    convert text to filesystem-friendly slug.
    """
    text = text.lower()
    #Replace non-alphanumeric characters with hyphens
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:max_length] or "untitled"

def build_filename(title: str, url: str, existing_names: set) -> str:
    """
    Generate a unique filename for a scraped source.
    """
    base_name = slugify(title) if title and title.lower() != 'n/a' else slugify(urlparse(url).netloc)
    candidate = base_name
    counter = 1
    while candidate in existing_names:
        candidate = f"{base_name}-{counter}"
        counter += 1
    existing_names.add(candidate)
    return f"{candidate}.md"

async def scrape_url(url: str, firecrawl_app: AsyncFirecrawl) -> dict:
    """
    Scrape a URL using Firecrawl with retries and return a dict with url, title, markdown.
    
    Uses maxAge = 1 week for 500% faster scraping by leveraging cached data when available.
    This optimization significantly improves performance for documentation, articles, and
    relatively static content while maintaining freshness within acceptable limits.
    """
    max_retries = 3
    base_delay = 5 #seconds
    timeout_seconds = 120000 #2 minutes timeout per request
    
    for attempt in range(max_retries):
        try:
            #Add timeout to individual Firecrawl request
            #Use maxAge for faster processing
            res = await firecrawl_app.scrape(
                url, formats=["markdown"], maxAge = MAX_AGE_ONE_WEEK, timeout = timeout_seconds
            )
            title = res.metadata.title if res and res.metadata and res.metadata.title else "N/A"
            markdown_content = res.markdown if ees and res.markdown else ""
            return {"url": url, "title": title, "markdown": markdown_content, "success": True}
        except asyncio.TimeoutError:
            error_msg = f"Firecrawl request timed out after {timeout_seconds}s for {url}"
            logger.warning(f"{error_msg} (attempt {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                delay = base_delay * (2**attempt)
                logging.warning(f"Retrying in {delay}s...")
                await asyncio.sleep(delay)
            else:
                logger.error(f"{error_msg} after {max_retries} attempts")
                return {
                    "url": url,
                    "title": "Scraping Timeout",
                    "markdown": f"{error_msg} after {max_retries} attempts.",
                    "success": False,
                }
        except Exception as e:
            #print the error with traceback
            logger.error(f"Error scraping {url}: {e}", exc_info = True)
            
            if attempt < max_retries - 1:
                delay = base_delay * (2**attempt)
                logger.warning(f"⚠️ Error scraping {url} (attempt {attempt + 1}/{max_retries}). Retrying in {delay}s...")
                await asyncio.sleep(delay)
            else:
                msg = f"⚠️ Error scraping {url} after {max_retries} attempts: {e}"
                logger.error(msg, exc_info=True)
                return {
                    "url": url,
                    "title": "Scraping Failed",
                    "markdown": msg,
                    "success": False,
                }
    return {
        "url": url,
        "title": "Scraping Failed",
        "markdown": f"Error scraping {url} after {max_retries} attempts."
        "success": False,
    }
    
def convert_markdown_images_to_urls(text: str) -> str:
    """
    Convert markdown images and linnk syntax to just URLs for image content.
    """
    pass