from knacr.errors.custom_exceptions import ValJsonEx
from knacr.library.loader import load_acr_db


def run() -> None:
    try:
        load_acr_db()
    except ValJsonEx:
        print("installed knacr version is not compatible with the latest data")


if __name__ == "__main__":
    run()
