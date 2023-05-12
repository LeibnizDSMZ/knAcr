import json
from pathlib import Path
from src.library.validate import validate_acr_db_schema


def run() -> None:
    data_path = Path(__file__).parent.joinpath(Path("../"), Path("data/acr_db.json"))
    with data_path.open() as fdb:
        validate_acr_db_schema(json.load(fdb))


if __name__ == "__main__":
    run()
