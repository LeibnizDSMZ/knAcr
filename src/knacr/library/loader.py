from importlib import resources
import json
from typing import Callable, Final, TypeVar

import requests
from knacr.constants.types import ACR_DB_T, ACR_MIN_DB_T, REG_DB_T
from knacr.container.fun.acr_db import create_acr_min_db
from knacr.errors.custom_exceptions import ReqURIEx, ValJsonEx
from knacr.library.validate import (
    validate_acr_db,
    validate_min_acr_db_schema,
    validate_regex_db,
)
from knacr import data


LATEST_VER: Final[str] = "latest"
STABLE_VER: Final[str] = "main"
CURRENT_VER: Final[str] = "v0.5.1"


def _load_data_from_file(db_name: str, /) -> bytes:
    with resources.files(data).joinpath(f"{db_name}.json").open("rb") as fhd:
        return fhd.read()


_T = TypeVar("_T", ACR_DB_T, ACR_MIN_DB_T, REG_DB_T)
_V = TypeVar("_V")


def _load_data(version: str, db_name: str, create: Callable[[_V], _T], /) -> _T:
    knacr = "https://raw.githubusercontent.com/StrainInfo/knAcr"
    req = f"{knacr}/{version}/src/knacr/data/{db_name}.json"
    if version == CURRENT_VER:
        print("loading from local file")
        return create(json.loads(_load_data_from_file(db_name)))
    print("downloading from github collection")
    if (res := requests.get(req, timeout=60)).ok:
        con = res.json()
        return create(con)
    else:
        raise ReqURIEx(f"Could not get {req}")


def load_acr_db(version: str = CURRENT_VER, /) -> ACR_DB_T:
    return _load_data(version, "acr_db", parse_acr_db)


def load_min_acr_db(version: str = CURRENT_VER, /) -> ACR_MIN_DB_T:
    return _load_data(version, "acr_db", parse_min_acr_db)


def load_regex_db(acr_db: ACR_DB_T, version: str = CURRENT_VER, /) -> REG_DB_T:
    return _load_data(
        version, "regex_db", lambda reg_db: parse_regex_db(reg_db, acr_db, True)
    )


_TJ = TypeVar("_TJ")


def parse_acr_db(acr_db: _TJ) -> ACR_DB_T:
    if not isinstance(acr_db, dict):
        raise ValJsonEx("JSON is not a dictionary")
    return validate_acr_db(acr_db)


def parse_min_acr_db(acr_db: _TJ) -> ACR_MIN_DB_T:
    if not isinstance(acr_db, dict):
        raise ValJsonEx("JSON is not a dictionary")
    validate_min_acr_db_schema(acr_db)
    return create_acr_min_db(acr_db)


def parse_regex_db(regex_db: _TJ, acr_db: ACR_DB_T, equal_sized: bool, /) -> REG_DB_T:
    if not isinstance(regex_db, dict):
        raise ValJsonEx("JSON is not a dictionary")
    return validate_regex_db(regex_db, acr_db, equal_sized)
