from typing import Final, TypeVar
import re

from jsonschema import ValidationError, validate
from knacr.container.acr_db import AcrCoreReg, AcrDb
from knacr.container.fun.acr_db import check_uri_template, create_acr_db
from knacr.errors.custom_exceptions import ValJsonEx

from knacr.schemas.acr_db import ACR_DB, ACR_MIN_DB

_TJ = TypeVar("_TJ")


_ACR: Final[re.Pattern[str]] = re.compile("^[A-Z:]+$")
_ACR_SPL: Final[re.Pattern[str]] = re.compile(":")


def _check_unique_gen(
    unique: set[tuple[str, str, str, str]], acr_db: AcrDb, /
) -> tuple[str, str, str, str]:
    unique_id = (acr_db.code, acr_db.acr, acr_db.name, acr_db.country)
    if unique_id in unique:
        raise ValJsonEx(f"{unique_id} was seen more than once, but should be unique")
    return unique_id


def _check_unique_ror(unique: set[tuple[str, str]], acr_db: AcrDb, /) -> tuple[str, str]:
    if acr_db.ror == "" or acr_db.deprecated:
        return "_", "_"
    unique_id = (acr_db.acr, acr_db.ror)
    if unique_id in unique:
        raise ValJsonEx(f"{unique_id} was seen more than once, but should be unique")
    return unique_id


def _check_changed_to_id(cur_acr_con: AcrDb, acr_db: dict[int, AcrDb], /) -> None:
    if cur_acr_con.deprecated and len(cur_acr_con.acr_synonym) > 0:
        raise ValJsonEx(
            f"{cur_acr_con.acr}: 'deprecated' can not have a 'synonyms' field"
        )
    if cur_acr_con.deprecated and len(cur_acr_con.acr_changed_to) > 0:
        raise ValJsonEx(
            f"{cur_acr_con.acr}: 'deprecated' can not have a 'changed to' field"
        )
    for acr_cha in cur_acr_con.acr_changed_to:
        next_acr_con = acr_db.get(acr_cha.id, None)
        if next_acr_con is None:
            raise ValJsonEx(f"missing 'changed to' acr id {acr_cha.id}")
        if next_acr_con.deprecated:
            raise ValJsonEx(
                f"{cur_acr_con.acr}: acr can not change into "
                + f"a deprecated acr {acr_cha.id}"
            )


def _check_missing_link_id(all_ids: set[int], /) -> None:
    for ind in range(1, max(all_ids) + 1):
        if ind not in all_ids:
            raise ValJsonEx(f"missing acr id {ind}")


def _check_acr(acr: str, /) -> None:
    if _ACR.match(acr) is None:
        raise ValJsonEx(f"{acr} does not comply to acronym standards ^[A-Z:]+$")


def _check_acr_in_reg(acr: str, ccno_reg: str, /) -> None:
    for acr_part in _ACR_SPL.split(acr):
        if acr_part not in ccno_reg:
            raise ValJsonEx(f"{acr} mismatches the acronym in regex: {ccno_reg}")


def _check_regex_start_end(reg_full: list[str], reg_part: list[str], /) -> None:
    for reg in reg_full:
        if reg[0] != r"^" or reg[-1] != r"$":
            raise ValJsonEx(f"invalid full regex {reg}")
    for reg in reg_part:
        if reg[0] == r"^" or reg[-1] == r"$":
            raise ValJsonEx(f"invalid part regex {reg}")


def _check_list_uniqueness(typ: str, con: list[str], /) -> None:
    if len(set(con)) != len(con):
        raise ValJsonEx(f"duplicates in {typ} - {con} found")


def _check_pre_suf(typ: str, pr_su: str, pr_su_con: list[str], /) -> None:
    if pr_su != "" and len(pr_su_con) == 0:
        raise ValJsonEx(f"{typ} defines {pr_su} but given list is empty")
    for ps_el in pr_su_con:
        if ps_el not in pr_su:
            raise ValJsonEx(f"given list for {typ} has unknown element {ps_el}")


def _check_regex(r_ccno: str, r_id: AcrCoreReg, /) -> None:
    _check_list_uniqueness("prefix", r_id.pre)
    _check_list_uniqueness("suffix", r_id.suf)
    _check_regex_start_end([r_ccno, r_id.full], [r_id.core, *r_id.pre, *r_id.suf])
    if len(r_id.full) <= 2:
        raise ValJsonEx(f"regex for id must be longer than 2 {r_id.full}")
    if r_id.full[1:] not in r_ccno:
        raise ValJsonEx(
            f"regex for ccno must contain regex for id: {r_id.full} -> {r_ccno}"
        )
    if (
        pre_suf := re.compile(rf"^(.*){re.escape(r_id.core)}(.*)$").match(r_id.full)
    ) is not None:
        pre, suf = pre_suf.groups()
        _check_pre_suf("prefix", pre[1:], r_id.pre)
        _check_pre_suf("suffix", suf[0:-2], r_id.suf)
    else:
        raise ValJsonEx(
            f"regex for id must contain regex for core: {r_id.core} -> {r_id.full}"
        )


def _check_loops(cur: AcrDb, full: dict[int, AcrDb], ids: set[int], /) -> None:
    for changed in cur.acr_changed_to:
        changed_to = full.get(changed.id, None)
        if changed.id in ids:
            raise ValJsonEx(f"loop detected in {ids} for {cur.acr}")
        if changed_to is None:
            raise ValJsonEx(f"missing changed to id {changed.id} for acronym {cur.acr}")
        ids.add(changed.id)
        _check_loops(changed_to, full, ids)


def _validate_acr_db_dc(to_eval_acr: dict[int, AcrDb], /) -> None:
    all_ids = set(to_eval_acr.keys())
    _check_missing_link_id(all_ids)
    unique_gen: set[tuple[str, str, str, str]] = set()
    unique_ror: set[tuple[str, str]] = set()
    for acr_id, acr_db in to_eval_acr.items():
        check_uri_template(acr_db.catalogue)
        unique_gen.add(_check_unique_gen(unique_gen, acr_db))
        unique_ror.add(_check_unique_ror(unique_ror, acr_db))
        _check_changed_to_id(acr_db, to_eval_acr)
        _check_acr(acr_db.acr)
        _check_regex(acr_db.regex_ccno, acr_db.regex_id)
        _check_acr_in_reg(acr_db.acr, acr_db.regex_ccno)
        _check_loops(acr_db, to_eval_acr, {acr_id})


def validate_acr_db(to_eval: _TJ, /) -> dict[int, AcrDb]:
    if not isinstance(to_eval, dict):
        raise ValJsonEx(f"expected a dictionary, got {type(to_eval)}")
    try:
        validate(instance=to_eval, schema=ACR_DB)
        acr_db = create_acr_db(to_eval)
        if len(acr_db) > 0:
            _validate_acr_db_dc(acr_db)
    except ValidationError as exc:
        raise ValJsonEx(
            f"Acronym Data is incorrectly formatted! [{exc.message}]"
        ) from exc
    else:
        return acr_db


def validate_min_acr_db_schema(to_eval: _TJ, /) -> None:
    if not isinstance(to_eval, dict):
        raise ValJsonEx(f"expected a dictionary, got {type(to_eval)}")
    try:
        validate(instance=to_eval, schema=ACR_MIN_DB)
    except ValidationError as exc:
        raise ValJsonEx(
            f"Acronym Data is incorrectly formatted! [{exc.message}]"
        ) from exc
