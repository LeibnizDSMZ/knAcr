from dataclasses import dataclass
from enum import Enum
from typing import final


class LinkLevel(Enum):
    cat = "catalogue"
    home = "homepage"
    emp = "no link found"


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class CatalogueLink:
    level: LinkLevel
    catalogue: str = ""
    homepage: str = ""
