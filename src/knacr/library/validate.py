from typing import TypeVar

from jsonschema import ValidationError, validate
from knacr.container.acr_db import AcrDb
from knacr.container.fun.acr_db import check_uri_template, create_acr_db
from knacr.errors.custom_exceptions import ValJsonEx

from knacr.schemas.acr_db import ACR_DB

_TJ = TypeVar("_TJ")


def _validate_acr_db_dc(to_eval_acr: dict[int, AcrDb], /) -> None:
    for ind in range(1, max(to_eval_acr.keys()) + 1):
        if ind not in to_eval_acr:
            raise ValJsonEx(f"missing acr id {ind}")
    uniqueness = set()
    for acr_db in to_eval_acr.values():
        check_uri_template(acr_db.catalogue)
        unique_id = (acr_db.code, acr_db.acr, acr_db.name)
        if unique_id in uniqueness:
            raise ValJsonEx(f"{unique_id} was seen more than once, but should be unique")
        uniqueness.add(unique_id)


def validate_acr_db_schema(to_eval: _TJ, /) -> None:
    if not isinstance(to_eval, dict):
        raise ValJsonEx(f"expected a dictionary, got {type(to_eval)}")
    try:
        validate(instance=to_eval, schema=ACR_DB)
        acr_db = create_acr_db(to_eval)
        if len(acr_db) > 0:
            _validate_acr_db_dc(acr_db)
    except ValidationError as exc:
        raise ValJsonEx(
            f"Acronym Data is incorrectly formatted! [{str(exc.cause)}]"
        ) from exc
