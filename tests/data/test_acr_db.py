import pytest
from src.errors.custom_exceptions import ValJsonEx
from src.main import run


def test_main_run() -> None:
    try:
        run()
    except ValJsonEx as val_ex:
        pytest.fail(f"acr data malformed - {val_ex.message}")
