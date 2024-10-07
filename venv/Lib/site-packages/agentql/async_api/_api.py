"""
This module is an entrypoint to AgentQL service
"""

from typing import Any, Coroutine

from playwright.async_api import Page as _Page

from agentql.ext.playwright.async_api import Page


async def wrap_async(page: Coroutine[Any, Any, _Page]) -> Page:
    """
    Casts a Playwright Async `Page` object to an AgentQL `Page` type to get access to the AgentQL's querying API.
    See `agentql.ext.playwright.async_api.Page` for API details.
    """
    return await page  # type: ignore
