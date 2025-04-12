import re


def make_valid_filename(text: str) -> str:
    return re.sub(
        r'[<>:"/\\|?*;]', "_", text
    )  # Replace invalid filename characters with underscores
