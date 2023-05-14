import json
import pytest

from knacr.errors.custom_exceptions import ValJsonEx
from knacr.library.loader import parse_acr_db


pytest_plugins = ("tests.fixture.data",)


def test_acr_db(load_fix_acr_db: bytes) -> None:
    try:
        parse_acr_db(json.loads(load_fix_acr_db))
    except ValJsonEx as val_ex:
        pytest.fail(f"acr data malformed - {val_ex.message}")
