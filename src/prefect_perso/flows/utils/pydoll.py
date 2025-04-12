import asyncio
import os
from pathlib import Path

import httpx
from prefect import task
from prefect.cache_policies import NO_CACHE
from pydoll.browser.options import Options
from pydoll.browser.page import Page
from pydoll.element import WebElement
from tqdm import tqdm


async def highlight(self, element: WebElement, time: int = 5) -> None:
    """
    Temporarily highlight a web element by adding a red border and then restoring its original style.

    Args:
        element (WebElement): The web element to highlight.
        time (int, optional): Duration of the highlight in seconds. Defaults to 5.

    Briefly draws attention to a specific web element by adding a red border with a smooth transition,
    then restores the element's original styling after a specified time interval.
    """
    original_style = element.get_attribute("style")
    await self.execute_script(
        """
    argument.style.border = '3px solid red';
    argument.style.transition = 'border 0.3s ease-in-out';
    """,
        element,
    )
    await asyncio.sleep(time)

    await self.execute_script(
        f"""
        argument.setAttribute('style', '{original_style}');
        """,
        element,
    )


Page.highlight = highlight


@task(cache_policy=NO_CACHE)
def get_options(
    headless: bool = False,
    chrome_user_data: str = os.path.join(os.getcwd(), "chrome_user_data"),
) -> Options:
    """
    Configure and return Chrome WebDriver options for web automation.

    Args:
        headless (bool, optional): Whether to run Chrome in headless mode. Defaults to False.
        chrome_user_data (str, optional): Path to Chrome user data directory.
            Defaults to a 'chrome_user_data' directory in the current working directory.

    Returns:
        Options: Configured Chrome WebDriver options with specific settings for web scraping.
    """
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--mute-audio")
    options.add_argument("--disable-dev-shm-usage")

    options.add_argument(f"--user-data-dir={chrome_user_data}")
    options.add_argument("--profile-directory=Default")
    return options


async def parallel_scrap(
    fn: callable,
    chunk_iterator: list,
    chunk_key: str,
    max_concurrent: int = 60,
    **kwargs,
) -> list:
    """
    Asynchronously scrape data with a maximum number of concurrent tasks.

    Args:
        fn (Callable): The async function to call for each element in the iterator.
        chunk_iterator (list): The list of elements to be processed.
        chunk_key (str): The key name to pass each element to the function.
        max_concurrent (int, optional): Maximum number of concurrent tasks. Defaults to 60.
        **kwargs: Additional keyword arguments to pass to the scraping function.

    Returns:
        list: Aggregated results from all processed elements.
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    all_data = []
    tasks = []

    async def process_item(element):
        async with semaphore:
            return await fn(**{chunk_key: element}, **kwargs)

    # Create all tasks
    for element in chunk_iterator:
        tasks.append(process_item(element))

    # Process tasks with progress bar
    for _task in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        result = await _task
        all_data.append(result)

    return all_data


async def download_media(
    media_url: str,
    destination_folder: Path,
    media_name: str,
    chunk_size: int = 8192,
) -> None:
    """
    Asynchronously downloads media from a URL with progress tracking.

    Args:
        media_url (str): The URL of the media to download.
        destination_folder (Path): The directory where the media will be saved.
        media_name (str): The name to give to the downloaded file, including extension.
        chunk_size (int, optional): Size of chunks to download at a time. Defaults to 8192 bytes.

    Returns:
        None

    Raises:
        httpx.RequestError: If the download request fails.
        OSError: If there are issues writing to the destination file.
    """
    async with httpx.AsyncClient() as client:
        async with client.stream("GET", media_url) as r:
            total_size = int(r.headers.get("content-length", 0))
            with tqdm(total=total_size, unit="B", unit_scale=True) as pbar:
                with open(destination_folder / media_name, "wb") as f:
                    async for chunk in r.aiter_bytes(chunk_size=chunk_size):
                        pbar.update(len(chunk))
                        f.write(chunk)
