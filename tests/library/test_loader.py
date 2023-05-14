import json
from unittest.mock import MagicMock, patch
import pytest

from knacr.errors.custom_exceptions import ValJsonEx, ReqURIEx
from knacr.library.loader import load_acr_db

pytest_plugins = ("tests.fixture.data",)


class TestLoader:
    @patch("knacr.library.loader.requests")
    def test_load_acr_db_success(self, req: MagicMock, load_fix_acr_db: bytes) -> None:
        resp = MagicMock()
        resp.ok = True
        resp.json.return_value = json.loads(load_fix_acr_db)
        req.get.return_value = resp
        try:
            load_acr_db()
        except (ValJsonEx, ReqURIEx) as val_ex:
            pytest.fail(f"acr data malformed - {val_ex.message}")

    @patch("knacr.library.loader.requests")
    def test_load_acr_db_fail(self, req: MagicMock) -> None:
        resp = MagicMock()
        resp.ok = False
        req.get.return_value = resp
        with pytest.raises(ReqURIEx):
            load_acr_db("never_tag")
