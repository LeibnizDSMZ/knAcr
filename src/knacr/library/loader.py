from importlib import resources
import json
from typing import Callable, Final, TypeVar

import requests
from knacr.container.acr_db import AcrDb
from knacr.container.fun.acr_db import create_acr_min_db
from knacr.errors.custom_exceptions import ReqURIEx, ValJsonEx
from knacr.library.validate import validate_acr_db, validate_min_acr_db_schema
from knacr import data


LATEST_VER: Final[str] = "latest"
STABLE_VER: Final[str] = "main"
CURRENT_VER: Final[str] = "v0.5.0"


def _load_acr_db_from_file() -> bytes:
    with resources.files(data).joinpath("acr_db.json").open("rb") as fhd:
        return fhd.read()


_T = TypeVar("_T", dict[int, AcrDb], dict[int, tuple[str, bool]])
_V = TypeVar("_V")


def _load_acr_db(version: str, create: Callable[[_V], _T], /) -> _T:
    knacr = "https://raw.githubusercontent.com/StrainInfo/knAcr"
    req = f"{knacr}/{version}/src/knacr/data/acr_db.json"
    if version == CURRENT_VER:
        print("loading from local file")
        return create(json.loads(_load_acr_db_from_file()))
    print("downloading from github collection")
    if (res := requests.get(req, timeout=60)).ok:
        con = res.json()
        return create(con)
    else:
        raise ReqURIEx(f"Could not get {req}")


def load_acr_db(version: str = CURRENT_VER, /) -> dict[int, AcrDb]:
    return _load_acr_db(version, parse_acr_db)


def load_min_acr_db(version: str = CURRENT_VER, /) -> dict[int, tuple[str, bool]]:
    return _load_acr_db(version, parse_min_acr_db)


_TJ = TypeVar("_TJ")


def parse_acr_db(acr_db: _TJ) -> dict[int, AcrDb]:
    if not isinstance(acr_db, dict):
        raise ValJsonEx("JSON is not a dictionary")
    return validate_acr_db(acr_db)


def parse_min_acr_db(acr_db: _TJ) -> dict[int, tuple[str, bool]]:
    if not isinstance(acr_db, dict):
        raise ValJsonEx("JSON is not a dictionary")
    validate_min_acr_db_schema(acr_db)
    return create_acr_min_db(acr_db)


_load_acr_db_from_file()
