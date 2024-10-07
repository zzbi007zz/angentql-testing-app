import logging
from datetime import datetime
from typing import TYPE_CHECKING, Literal, Optional, Tuple, Union

from playwright.async_api import Page as _Page
from playwright.async_api import Response
from playwright_stealth import StealthConfig, stealth_async

from agentql import AccessibilityTreeError, QueryParser, trail_logger
from agentql._core._api_constants import DEFAULT_RESPONSE_MODE
from agentql._core._syntax.node import ContainerNode
from agentql._core._typing import ResponseMode
from agentql._core._utils import minify_query
from agentql.async_api._agentql_service import query_agentql_server
from agentql.async_api._debug_manager import DebugManager
from agentql.ext.playwright._driver_constants import (
    DEFAULT_INCLUDE_ARIA_HIDDEN,
    DEFAULT_QUERY_DATA_TIMEOUT_SECONDS,
    DEFAULT_QUERY_ELEMENTS_TIMEOUT_SECONDS,
    DEFAULT_WAIT_FOR_NETWORK_IDLE,
    RENDERER,
    USER_AGENT,
    VENDOR,
)
from agentql.ext.playwright._network_monitor import PageActivityMonitor
from agentql.ext.playwright._utils import post_process_accessibility_tree
from agentql.ext.playwright.async_api.response_proxy import AQLResponseProxy, Locator

from .._utils import find_element_by_id, post_process_accessibility_tree
from ._utils_async import (
    add_dom_change_listener_shared,
    add_request_event_listeners_for_page_monitor_shared,
    determine_load_state_shared,
    get_page_accessibility_tree,
    process_iframes,
)

log = logging.getLogger("agentql")


class Page(_Page):
    if TYPE_CHECKING:

        async def goto(
            self,
            url: str,
            *,
            timeout: Optional[float] = None,
            wait_until: Optional[
                Literal["commit", "domcontentloaded", "load", "networkidle"]
            ] = "domcontentloaded",
            referer: Optional[str] = None,
        ) -> Optional[Response]:
            """
            AgentQL's `page.goto()` override that uses `domcontentloaded` as the default value for the `wait_until` parameter.
            This change addresses issue with the `load` event not being reliably fired on some websites.

            For parameters information and original method's documentation, please refer to
            [Playwright's documentation](https://playwright.dev/docs/api/class-page#page-goto)
            """

        async def get_by_prompt(
            self,
            prompt: str,
            timeout: int = DEFAULT_QUERY_ELEMENTS_TIMEOUT_SECONDS,
            wait_for_network_idle: bool = DEFAULT_WAIT_FOR_NETWORK_IDLE,
            include_aria_hidden: bool = DEFAULT_INCLUDE_ARIA_HIDDEN,
            mode: ResponseMode = DEFAULT_RESPONSE_MODE,
        ) -> Union[Locator, None]:
            """
            Returns a single web element located by a natural language prompt (as opposed to a AgentQL query).

            Parameters:
            -----------
            prompt (str): The natural language description of the element to locate.
            timeout (int) (optional): Timeout value in seconds for the connection with backend API service.
            wait_for_network_idle (bool) (optional): Whether to wait for network reaching full idle state before querying the page. If set to `False`, this method will only check for whether page has emitted [`load` event](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event).
            include_aria_hidden (bool) (optional): Whether to include elements with `aria-hidden` attribute in the accessibility tree.
            mode (ResponseMode) (optional): The mode of the query. It can be either 'standard' or 'fast'.

            Returns:
            --------
            Playwright [Locator](https://playwright.dev/python/docs/api/class-locator) | None: The found element or `None` if no matching elements were found.
            """

        async def query_elements(
            self,
            query: str,
            timeout: int = DEFAULT_QUERY_ELEMENTS_TIMEOUT_SECONDS,
            wait_for_network_idle: bool = DEFAULT_WAIT_FOR_NETWORK_IDLE,
            include_aria_hidden: bool = DEFAULT_INCLUDE_ARIA_HIDDEN,
            mode: ResponseMode = DEFAULT_RESPONSE_MODE,
        ) -> AQLResponseProxy:  # type: ignore 'None' warning
            """
            Queries the web page for multiple web elements that match the AgentQL query.

            Parameters:
            ----------
            query (str): An AgentQL query in String format.
            timeout (int) (optional): Timeout value in seconds for the connection with backend API service.
            wait_for_network_idle (bool) (optional): Whether to wait for network reaching full idle state before querying the page. If set to `False`, this method will only check for whether page has emitted [`load` event](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event).
            include_aria_hidden (bool) (optional): Whether to include elements with `aria-hidden` attribute in the accessibility tree.
            mode (ResponseMode) (optional): The mode of the query. It can be either 'standard' or 'fast'.

            Returns:
            -------
            AQLResponseProxy: The AgentQL response object with elements that match the query. Response provides access to requested elements via its fields.
            """

        async def query_data(
            self,
            query: str,
            timeout: int = DEFAULT_QUERY_DATA_TIMEOUT_SECONDS,
            wait_for_network_idle: bool = DEFAULT_WAIT_FOR_NETWORK_IDLE,
            include_aria_hidden: bool = DEFAULT_INCLUDE_ARIA_HIDDEN,
            mode: ResponseMode = DEFAULT_RESPONSE_MODE,
        ) -> dict:  # type: ignore 'None' warning
            """
            Queries the web page for data that matches the AgentQL query, such as blocks of text or numbers.

            Parameters:
            ----------
            query (str): An AgentQL query in String format.
            timeout (int) (optional): Timeout value in seconds for the connection with backend API service.
            wait_for_network_idle (bool) (optional): Whether to wait for network reaching full idle state before querying the page. If set to `False`, this method will only check for whether page has emitted [`load` event](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event).
            include_aria_hidden (bool) (optional): Whether to include elements with `aria-hidden` attribute in the accessibility tree.
            mode (ResponseMode) (optional): The mode of the query. It can be either 'standard' or 'fast'.

            Returns:
            -------
            dict: Data that matches the query.
            """

        async def wait_for_page_ready_state(
            self, wait_for_network_idle: bool = DEFAULT_WAIT_FOR_NETWORK_IDLE
        ):
            """
            Waits for the page to reach the "Page Ready" state, i.e. page has entered a relatively stable state and most main content is loaded. Might be useful before triggering an AgentQL query or any other interaction for slowly rendering pages.

            Parameters:
            -----------
            wait_for_network_idle (bool) (optional): Whether to wait for network reaching full idle state. If set to `False`, this method will only check for whether page has emitted [`load` event](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event).
            """

        async def enable_stealth_mode(
            self,
            webgl_vendor: str = VENDOR,
            webgl_renderer: str = RENDERER,
            nav_user_agent: str = USER_AGENT,
        ):
            """
            Enables "stealth mode" with given configuration. To avoid being marked as a bot, parameters' values should match the real values used by your device.
            Use browser fingerprinting websites such as https://bot.sannysoft.com and https://pixelscan.net for realistic examples.

            Parameters:
            -----------
            webgl_vendor (str) (optional):
                The vendor of the GPU used by WebGL to render graphics, such as `Apple Inc.`. After setting this parameter, your browser will emit this vendor information.
            webgl_renderer (str) (optional):
                Identifies the specific GPU model or graphics rendering engine used by WebGL, such as `Apple M3`. After setting this parameter, your browser will emit this renderer information.
            nav_user_agent (str) (optional):
                Identifies the browser, its version, and the operating system, such as `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36`. After setting this parameter, your browser will send this user agent information to the website.
            """


async def _goto(
    self,
    url: str,
    *,
    timeout: Optional[float] = None,
    wait_until: Optional[
        Literal["commit", "domcontentloaded", "load", "networkidle"]
    ] = "domcontentloaded",
    referer: Optional[str] = None,
) -> Optional[Response]:
    # pylint: disable=W0212
    if self._page_monitor is None:
        self._page_monitor = PageActivityMonitor()
        await add_request_event_listeners_for_page_monitor_shared(self, self._page_monitor)

    result = await self._original_goto(
        url=url, timeout=timeout, wait_until=wait_until, referer=referer
    )

    await add_dom_change_listener_shared(self)
    return result


async def _get_by_prompt(
    self,
    prompt: str,
    timeout: int = DEFAULT_QUERY_ELEMENTS_TIMEOUT_SECONDS,
    wait_for_network_idle: bool = DEFAULT_WAIT_FOR_NETWORK_IDLE,
    include_aria_hidden: bool = DEFAULT_INCLUDE_ARIA_HIDDEN,
    mode: ResponseMode = DEFAULT_RESPONSE_MODE,
) -> Union[Locator, None]:
    query = f"""
{{
    page_element({prompt})
}}
"""
    response, _ = await _execute_query(
        self,
        query=query,
        timeout=timeout,
        include_aria_hidden=include_aria_hidden,
        wait_for_network_idle=wait_for_network_idle,
        mode=mode,
        is_data_query=False,
    )
    response_data = response.get("page_element")
    if not response_data:
        return None

    tf623_id = response_data.get("tf623_id")
    iframe_path = response_data.get("attributes", {}).get("iframe_path")
    web_element = find_element_by_id(page=self, tf623_id=tf623_id, iframe_path=iframe_path)

    return web_element  # type: ignore


async def _query_elements(
    self,
    query: str,
    timeout: int = DEFAULT_QUERY_ELEMENTS_TIMEOUT_SECONDS,
    wait_for_network_idle: bool = DEFAULT_WAIT_FOR_NETWORK_IDLE,
    include_aria_hidden: bool = DEFAULT_INCLUDE_ARIA_HIDDEN,
    mode: ResponseMode = DEFAULT_RESPONSE_MODE,
) -> AQLResponseProxy:
    response, query_tree = await _execute_query(
        self,
        query=query,
        timeout=timeout,
        include_aria_hidden=include_aria_hidden,
        wait_for_network_idle=wait_for_network_idle,
        mode=mode,
        is_data_query=False,
    )
    return AQLResponseProxy(response, self, query_tree)


async def _query_data(
    self,
    query: str,
    timeout: int = DEFAULT_QUERY_DATA_TIMEOUT_SECONDS,
    wait_for_network_idle: bool = DEFAULT_WAIT_FOR_NETWORK_IDLE,
    include_aria_hidden: bool = DEFAULT_INCLUDE_ARIA_HIDDEN,
    mode: ResponseMode = DEFAULT_RESPONSE_MODE,
) -> dict:
    response, _ = await _execute_query(
        self,
        query=query,
        timeout=timeout,
        include_aria_hidden=include_aria_hidden,
        wait_for_network_idle=wait_for_network_idle,
        mode=mode,
        is_data_query=True,
    )
    return response


async def _execute_query(
    page: Page,
    query: str,
    timeout: int,
    wait_for_network_idle: bool,
    include_aria_hidden: bool,
    mode: ResponseMode,
    is_data_query: bool,
) -> Tuple[dict, ContainerNode]:
    trail_logger.add_event(f"Querying {minify_query(query)} on {page}")
    log.debug(f"Querying {'data' if is_data_query else 'elements'}: {query}")

    query_tree = QueryParser(query).parse()

    await page.wait_for_page_ready_state(wait_for_network_idle=wait_for_network_idle)

    if DebugManager.debug_mode_enabled:
        date = datetime.now().astimezone().strftime("%Y-%m-%d_%H-%M-%S.%f%z").replace("+", "Z")
        await page.screenshot(
            path=f"{DebugManager.debug_files_path}/screenshot_{date}.png",
            full_page=True,
        )

    try:
        accessibility_tree = await get_page_accessibility_tree(
            page, include_aria_hidden=include_aria_hidden
        )
        await process_iframes(page, accessibility_tree)
        post_process_accessibility_tree(accessibility_tree)

    except Exception as e:
        raise AccessibilityTreeError() from e

    if DebugManager.debug_mode_enabled:
        DebugManager.set_accessibility_tree(accessibility_tree)

    log.info(
        f"AgentQL query execution may take longer than expected, especially for complex queries and lengthy webpages. If you notice no activity in the logs, please be patient—the query is still in progress and has not frozen. The current timeout is set to {timeout} seconds, so you can expect a response within that timeframe. If a timeout error occurs, consider extending the timeout duration to give AgentQL backend more time to finish the work."
    )

    response = await query_agentql_server(
        query, accessibility_tree, timeout, page.url, mode, is_data_query
    )

    return response, query_tree


# pylint: disable=W0212
async def _wait_for_page_ready_state(
    self, wait_for_network_idle: bool = DEFAULT_WAIT_FOR_NETWORK_IDLE
):
    trail_logger.add_event(f"Waiting for {self} to reach 'Page Ready' state")

    # Wait for the page to reach the "Page Ready" state
    await determine_load_state_shared(
        page=self, monitor=self._page_monitor, wait_for_network_idle=wait_for_network_idle
    )

    # Reset the network monitor to clear the existing state
    if self._page_monitor:
        self._page_monitor.reset()

    trail_logger.add_event(f"Finished waiting for {self} to reach 'Page Ready' state")


async def _enable_stealth_mode(
    self,
    webgl_vendor: str = VENDOR,
    webgl_renderer: str = RENDERER,
    nav_user_agent: str = USER_AGENT,
):
    await stealth_async(
        self,
        config=StealthConfig(
            vendor=webgl_vendor,
            renderer=webgl_renderer,
            # nav_user_agent will only take effect when navigator_user_agent parameter is True
            nav_user_agent=nav_user_agent,
            navigator_user_agent=nav_user_agent is not None,
        ),
    )


# Add the get_by_ai method to the Page class
setattr(_Page, "get_by_prompt", _get_by_prompt)

setattr(_Page, "query_elements", _query_elements)

setattr(_Page, "query_data", _query_data)

setattr(_Page, "wait_for_page_ready_state", _wait_for_page_ready_state)

setattr(_Page, "enable_stealth_mode", _enable_stealth_mode)

setattr(_Page, "_page_monitor", None)

# Bind original `page.goto()` method to a new name before it's overridden.
# This line should be executed before `setattr(_Page, "goto", _goto)` to avoid infinite recursion.
setattr(_Page, "_original_goto", _Page.goto)

setattr(_Page, "goto", _goto)
