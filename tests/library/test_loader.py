import pytest
from src.errors.custom_exceptions import ReqURIEx, ValJsonEx
from src.library.loader import load_acr_db


def test_loader() -> None:
    with pytest.raises(ReqURIEx):
        load_acr_db("never_tag")
    try:
        load_acr_db()
    except (ValJsonEx, ReqURIEx) as val_ex:
        pytest.fail(f"acr data malformed - {val_ex.message}")
