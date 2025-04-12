import asyncio

from prefect import flow
from pydoll.browser.chrome import Chrome

from src.prefect_perso.utils.pydoll import get_options


@flow(name="Inactive browser")
async def main() -> None:
    """The point of this flow is to pop an inactive browser so we can manually interact with website while retaining user data (e.g. Amazon logging)"""
    browser = Chrome(options=get_options(headless=False))
    await browser.start()
    await asyncio.sleep(3600)
    await browser.__aexit__(exc_tb="", exc_type="", exc_val="")
