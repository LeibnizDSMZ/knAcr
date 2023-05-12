from typing import Final

import requests
from src.container.acr_db import AcrDb
from src.container.fun.acr_db import create_acr_db
from src.errors.custom_exceptions import ReqURIEx, ValJsonEx
from src.library.validate import validate_acr_db_schema


LATEST_VER: Final[str] = "latest"


def load_acr_db(version: str = LATEST_VER, /) -> dict[int, AcrDb]:
    req = f"https://raw.githubusercontent.com/artdotlis/knAcr/{version}/data/acr_db.json"
    print("downloading from github collection")
    if (res := requests.get(req, timeout=60)).ok:
        con = res.json()
        if not isinstance(con, dict):
            raise ValJsonEx("JSON is not a dictionary")
        validate_acr_db_schema(con)
        return create_acr_db(con)
    else:
        raise ReqURIEx(f"Could not get {req}")
