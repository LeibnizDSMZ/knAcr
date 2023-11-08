from importlib import resources
import subprocess
import pytest
from knacr import data


@pytest.fixture()
def load_fix_acr_db() -> bytes:
    with resources.files(data).joinpath("acr_db.json").open("rb") as fhd:
        return fhd.read()


@pytest.fixture()
def load_fix_min_main_acr_db() -> bytes:
    sub_proc = subprocess.Popen(
        ["git", "show", "origin/main:data/acr_db.json"],  # noqa: S607
        shell=False,  # noqa: S603
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    out, err = sub_proc.communicate()
    if not out or err:
        pytest.fail(f"could not read from main acr_db {err!s}")
    return out.encode("utf-8")
