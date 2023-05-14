from pathlib import Path
import pytest


@pytest.fixture()
def load_fix_acr_db() -> bytes:
    with Path(__file__).parent.joinpath(Path("../" * 2), Path("data/acr_db.json")).open(
        "rb"
    ) as fhd:
        return fhd.read()
