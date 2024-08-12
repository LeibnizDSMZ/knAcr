import re
from urllib.parse import unquote_plus
from uuid import UUID
from pydantic import HttpUrl


def url_to_str(url: HttpUrl | None, /) -> str:
    if url is None:
        return ""
    return unquote_plus(url.unicode_string())


def uuid_to_str(uuid: UUID | None, /) -> str:
    if uuid is None:
        return ""
    return str(uuid)


def is_regex(val: str) -> str:
    try:
        re.compile(val)
    except re.error as err:
        raise ValueError("Regex has a wrong format") from err
    return val
