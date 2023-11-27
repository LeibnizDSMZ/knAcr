from typing import TypeAlias

from knacr.container.acr_db import AcrDbEntry


ACR_DB_T: TypeAlias = dict[int, AcrDbEntry]
ACR_MIN_DB_T: TypeAlias = dict[int, tuple[str, bool]]
CCNO_DB_T: TypeAlias = dict[int, list[str]]
