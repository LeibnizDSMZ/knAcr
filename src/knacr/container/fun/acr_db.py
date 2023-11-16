from collections import defaultdict
from dataclasses import asdict
from re import Pattern
import re
from typing import Any, Callable, Final, Mapping, TypeVar

from knacr.container.acr_db import AcrDbEntry, AcrChaT, CatArgs
from dacite import from_dict
from knacr.errors.custom_exceptions import ValJsonEx


def get_brc_merge_type() -> list[str]:
    return [str(cha.value) for cha in AcrChaT]


_TJ = TypeVar("_TJ", bound=Mapping[str, Any])


def _amend_regex_id(acr_db: dict[int, AcrDbEntry], /) -> dict[int, AcrDbEntry]:
    for acr_id, acr_con in acr_db.items():
        if acr_con.regex_id.core == "":
            buf = asdict(acr_con)
            buf.get("regex_id", {})["core"] = acr_con.regex_id.full[1:-2]
            acr_db[acr_id] = from_dict(data_class=AcrDbEntry, data=buf)
    return acr_db


def create_acr_db(to_eval: dict[str, _TJ], /) -> dict[int, AcrDbEntry]:
    acr_db = {
        int(acr_id): from_dict(data_class=AcrDbEntry, data=acr_db_entry)
        for acr_id, acr_db_entry in to_eval.items()
    }
    return _amend_regex_id(acr_db)


def create_acr_min_db(to_eval: dict[str, _TJ], /) -> dict[int, tuple[str, bool]]:
    min_db: dict[int, tuple[str, bool]] = {}
    for acr_id, db_ent in to_eval.items():
        if not isinstance(db_ent, dict):
            raise ValJsonEx(f"expected dict got {type(db_ent)} for id {acr_id}")
        acr = db_ent.get("acr", None)
        acr_dep = db_ent.get("deprecated", False)
        if not isinstance(acr, str):
            raise ValJsonEx(f"ID {acr_id} does not define an acronym {db_ent!s}")
        if not isinstance(acr_dep, bool):
            raise ValJsonEx(f"ID {acr_id} does not define deprecation status {db_ent!s}")
        min_db[int(acr_id)] = (acr, acr_dep)
    return min_db


_CAT_ACR: Final[Pattern[str]] = re.compile(r"\{acr\}")
_CAT_ID: Final[Pattern[str]] = re.compile(r"\{id\}")
_CAT_PRE: Final[Pattern[str]] = re.compile(r"\{pre\}")
_CAT_CORE: Final[Pattern[str]] = re.compile(r"\{core(:\d+)?\}")
_CAT_CORE_0: Final[Pattern[str]] = re.compile(r"\{core0(:\d+)?\}")
_CAT_SUF: Final[Pattern[str]] = re.compile(r"\{suf\}")

_OPT_VAL: Final[Pattern[str]] = re.compile(r"({[^{]+})?<.+?>({.+?})?")

_VALID_URI: Final[Pattern[str]] = re.compile(r"\{([^}]+?)\}")
_VALID_PAR: Final[set[str]] = {"acr", "id", "pre", "core", "core0", "suf"}
_VALID_PAR_SUB: Final[set[str]] = {"core", "core0"}
_ID_SUB: Final[Pattern[str]] = re.compile(r"^(.+?)(:\d+)?$")
_ID_SEP: Final[Pattern[str]] = re.compile(r"[^A-Za-z0-9]")


def check_uri_template(uri: str, /) -> None:
    sub_parts = defaultdict(list)
    for param in _VALID_URI.findall(uri):
        arg_parts = _ID_SUB.match(param)
        if arg_parts is None or arg_parts.group(1) not in _VALID_PAR:
            raise ValJsonEx(f"invalid param name detected [{param}]")
        if arg_parts.group(2) is not None:
            sub_parts[arg_parts.group(1)].append(int(arg_parts.group(2).strip(":")))
            if arg_parts.group(1) not in _VALID_PAR_SUB:
                raise ValJsonEx(
                    f"only {_VALID_PAR_SUB!s} are allowed to be defined as arrays"
                )
    for param, arr_id in sub_parts.items():
        if 0 in arr_id:
            raise ValJsonEx(f"zeros are not allowed as index for params [{param}]")


def _parse_id_core(mat: str, id_core: str, /) -> dict[str, str]:
    ids = _ID_SEP.split(id_core)
    num = _CAT_CORE.match(mat)
    if num is None:
        raise ValJsonEx(f"mismatched core id tag: {mat} -> {id_core}")
    if num.group(1) is None or num.group(1) == "":
        return {mat: id_core}
    id_num = int(num.group(1).strip(":"))
    if id_num > len(ids):
        return {mat: ""}
    return {mat: ids[id_num - 1]}


def _parse_id_core_0(mat: str, id_core: str, /) -> dict[str, str]:
    ids = _ID_SEP.split(id_core)
    num = _CAT_CORE_0.match(mat)
    if num is None:
        raise ValJsonEx(f"mismatched core0 id tag: {mat} -> {id_core}")
    if len(ids) > 1:
        raise ValJsonEx(
            f"zero core only available for integer structured ids: {mat} -> {id_core}"
        )
    id_num = int(num.group(1).strip(":"))
    return {mat: "0" * (id_num - len(id_core)) + id_core}


_REPL_PARAM: Final[dict[Pattern[str], Callable[[str, CatArgs], dict[str, str]]]] = {
    _CAT_ACR: lambda mat, cat: {mat: cat.acr},
    _CAT_ID: lambda mat, cat: {mat: cat.id},
    _CAT_PRE: lambda mat, cat: {mat: cat.pre},
    _CAT_CORE: lambda mat, cat: _parse_id_core(mat, cat.core),
    _CAT_CORE_0: lambda mat, cat: _parse_id_core_0(mat, cat.core),
    _CAT_SUF: lambda mat, cat: {mat: cat.suf},
}


def _get_repl_param_fun(
    href_part: str, /
) -> tuple[str, Callable[[str, CatArgs], dict[str, str]]] | None:
    for che, repl in _REPL_PARAM.items():
        if (mat := che.search(href_part)) is not None:
            return mat.group(0), repl
    return None


def _rm_opt(href: str, left: str, right: str, /) -> str:
    return re.compile(re.escape(left) + r"<.+?>" + re.escape(right)).sub(
        f"{left}{right}", href, 1
    )


def _get_left_right(
    left: str, right: str, args: CatArgs, /
) -> tuple[dict[str, str], dict[str, str]]:
    left_f, right_f = _get_repl_param_fun(left), _get_repl_param_fun(right)
    if left_f is None or right_f is None:
        raise ValJsonEx(f"uri contains unknown parameter names: {left} - {right}")
    return left_f[1](left_f[0], args), right_f[1](right_f[0], args)


def _are_params_empty(param_con: dict[str, str], /) -> bool:
    for p_val in param_con.values():
        if p_val != "":
            return False
    return True


def _fix_opt(href: str, match: tuple[str, str], args: CatArgs, /) -> str:
    left, right = match
    if "" in [left, right]:
        return _rm_opt(href, left, right)
    left_p, right_p = _get_left_right(left, right, args)
    if _are_params_empty(left_p) or _are_params_empty(right_p):
        return _rm_opt(href, left, right)
    return re.compile(re.escape(left) + r"<(.+?)>" + re.escape(right)).sub(
        rf"{left}\g<1>{right}", href, 1
    )


def replace_param_value(href: str, args: CatArgs, /) -> str:
    for opt in _OPT_VAL.findall(href):
        href = _fix_opt(href, opt, args)
    for che, repl in _REPL_PARAM.items():
        for mat in che.finditer(href):
            for to_repl, repl_val in repl(mat.group(0), args).items():
                href = href.replace(to_repl, repl_val)
    return href
