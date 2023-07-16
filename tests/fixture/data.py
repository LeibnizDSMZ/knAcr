from pathlib import Path
import subprocess
import pytest


@pytest.fixture()
def load_fix_acr_db() -> bytes:
    with Path(__file__).parent.joinpath(Path("../" * 2), Path("data/acr_db.json")).open(
        "rb"
    ) as fhd:
        return fhd.read()


@pytest.fixture()
def load_fix_min_acr_db() -> bytes:
    sub_proc = subprocess.Popen(
        ["/usr/bin/git", "show", "main:data/acr_db.json"],
        shell=False,  # noqa: S603
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    out, err = sub_proc.communicate()
    if not out or err:
        pytest.fail(f"could not read from main acr_db {err!s}")
    return out.encode("utf-8")
