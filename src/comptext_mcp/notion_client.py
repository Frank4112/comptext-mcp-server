"""Notion API Client für CompText MCP-Server - Production Ready"""
from notion_client import Client
from notion_client.errors import APIResponseError
from typing import Optional, List, Dict, Any
import os
import logging
import time
from functools import lru_cache, wraps

from .constants import (
    CACHE_SIZE,
    DEFAULT_DATABASE_ID,
    MAX_RETRIES,
    RETRY_DELAY,
    BACKOFF_FACTOR
)
from .utils import validate_page_id, validate_query_string, sanitize_text_output

# Logging Setup
logger = logging.getLogger(__name__)

# Configuration
NOTION_TOKEN = os.getenv("NOTION_API_TOKEN")
CODEX_DB_ID = os.getenv("COMPTEXT_DATABASE_ID", DEFAULT_DATABASE_ID)

if not NOTION_TOKEN:
    raise ValueError("NOTION_API_TOKEN environment variable is required")

# Initialize Notion Client
notion = Client(auth=NOTION_TOKEN)


class NotionClientError(Exception):
    """Custom exception for Notion client errors"""
    pass


def retry_on_failure(max_retries: int = MAX_RETRIES):
    """Decorator to retry function on failure with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except APIResponseError as e:
                    retries += 1
                    if retries >= max_retries:
                        logger.error(f"Max retries reached for {func.__name__}: {e}")
                        raise NotionClientError(f"Failed after {max_retries} retries: {e}")
                    
                    wait_time = RETRY_DELAY * (BACKOFF_FACTOR ** (retries - 1))
                    logger.warning(f"Retry {retries}/{max_retries} for {func.__name__} after {wait_time}s: {e}")
                    time.sleep(wait_time)
                except Exception as e:
                    logger.error(f"Unexpected error in {func.__name__}: {e}")
                    raise NotionClientError(f"Unexpected error: {e}")
            return None
        return wrapper
    return decorator


def _extract_text_from_rich_text(rich_text: List[Dict]) -> str:
    """Extract plain text from Notion rich text objects"""
    if not rich_text:
        return ""
    text = "".join([rt.get("plain_text", "") for rt in rich_text])
    return sanitize_text_output(text)


def _get_property_value(page: Dict, prop_name: str, prop_type: str) -> Any:
    """Extract property value based on type"""
    try:
        prop = page["properties"].get(prop_name, {})
        
        if prop_type == "title":
            return _extract_text_from_rich_text(prop.get("title", []))
        elif prop_type == "rich_text":
            return _extract_text_from_rich_text(prop.get("rich_text", []))
        elif prop_type == "select":
            select_data = prop.get("select")
            return select_data.get("name") if select_data else None
        elif prop_type == "multi_select":
            return [ms.get("name") for ms in prop.get("multi_select", [])]
        elif prop_type == "url":
            return prop.get("url")
        else:
            return None
    except Exception as e:
        logger.warning(f"Error extracting property {prop_name}: {e}")
        return None


def parse_page(page: Dict) -> Dict[str, Any]:
    """Parse Notion page to CompText format"""
    return {
        "id": page["id"],
        "url": page["url"],
        "titel": _get_property_value(page, "Titel", "title"),
        "beschreibung": _get_property_value(page, "Beschreibung", "rich_text"),
        "modul": _get_property_value(page, "Modul", "select"),
        "typ": _get_property_value(page, "Typ", "select"),
        "tags": _get_property_value(page, "Tags", "multi_select"),
        "created_time": page.get("created_time"),
        "last_edited_time": page.get("last_edited_time")
    }


def _block_to_text(block: Dict) -> str:
    """Convert a single block to text"""
    block_type = block.get("type")
    
    if block_type == "paragraph":
        return _extract_text_from_rich_text(block["paragraph"].get("rich_text", []))
    elif block_type == "heading_1":
        return f"# {_extract_text_from_rich_text(block['heading_1'].get('rich_text', []))}"
    elif block_type == "heading_2":
        return f"## {_extract_text_from_rich_text(block['heading_2'].get('rich_text', []))}"
    elif block_type == "heading_3":
        return f"### {_extract_text_from_rich_text(block['heading_3'].get('rich_text', []))}"
    elif block_type == "bulleted_list_item":
        return f"- {_extract_text_from_rich_text(block['bulleted_list_item'].get('rich_text', []))}"
    elif block_type == "numbered_list_item":
        return f"1. {_extract_text_from_rich_text(block['numbered_list_item'].get('rich_text', []))}"
    elif block_type == "code":
        code = _extract_text_from_rich_text(block["code"].get("rich_text", []))
        lang = block["code"].get("language", "")
        return f"```{lang}\n{code}\n```"
    elif block_type == "quote":
        return f"> {_extract_text_from_rich_text(block['quote'].get('rich_text', []))}"
    else:
        return ""


def blocks_to_text(blocks: List[Dict]) -> str:
    """Convert list of blocks to markdown text"""
    return "\n\n".join([_block_to_text(block) for block in blocks if _block_to_text(block)])


@lru_cache(maxsize=CACHE_SIZE)
@retry_on_failure()
def get_all_modules() -> List[Dict[str, Any]]:
    """Load all modules from CompText Codex (cached with retry logic)"""
    response = notion.databases.query(database_id=CODEX_DB_ID)
    return [parse_page(page) for page in response["results"]]


@retry_on_failure()
def get_module_by_name(modul_name: str) -> List[Dict[str, Any]]:
    """Load all entries of a specific module"""
    response = notion.databases.query(
        database_id=CODEX_DB_ID,
        filter={
            "property": "Modul",
            "select": {"equals": modul_name}
        }
    )
    return [parse_page(page) for page in response["results"]]


@retry_on_failure()
def get_page_content(page_id: str) -> str:
    """Load full content of a page"""
    validated_id = validate_page_id(page_id)
    blocks = notion.blocks.children.list(block_id=validated_id)
    return blocks_to_text(blocks["results"])


def search_codex(query: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """Search in CompText Codex"""
    validated_query = validate_query_string(query)
    all_modules = get_all_modules()
    query_lower = validated_query.lower()
    
    results = []
    for module in all_modules:
        titel = (module.get("titel") or "").lower()
        beschreibung = (module.get("beschreibung") or "").lower()
        tags = " ".join(module.get("tags", [])).lower()
        
        if query_lower in titel or query_lower in beschreibung or query_lower in tags:
            results.append(module)
            
            if len(results) >= max_results:
                break
    
    return results


@retry_on_failure()
def get_page_by_id(page_id: str) -> Dict[str, Any]:
    """Get page info by ID"""
    validated_id = validate_page_id(page_id)
    page = notion.pages.retrieve(page_id=validated_id)
    return parse_page(page)


@retry_on_failure()
def get_modules_by_tag(tag: str) -> List[Dict[str, Any]]:
    """Filter modules by tag"""
    response = notion.databases.query(
        database_id=CODEX_DB_ID,
        filter={
            "property": "Tags",
            "multi_select": {"contains": tag}
        }
    )
    return [parse_page(page) for page in response["results"]]


@retry_on_failure()
def get_modules_by_type(typ: str) -> List[Dict[str, Any]]:
    """Filter modules by type"""
    response = notion.databases.query(
        database_id=CODEX_DB_ID,
        filter={
            "property": "Typ",
            "select": {"equals": typ}
        }
    )
    return [parse_page(page) for page in response["results"]]


def clear_cache():
    """Clear LRU cache"""
    get_all_modules.cache_clear()
    logger.info("Cache cleared")
