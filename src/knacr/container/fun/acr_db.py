from re import Pattern
import re
from typing import Callable, Final, TypeVar

from knacr.container.acr_db import AcrDb, AcrChaT, CatArgs
from dacite import from_dict
from knacr.errors.custom_exceptions import ValJsonEx


def get_brc_merge_type() -> list[str]:
    return [str(cha.value) for cha in AcrChaT]


_TJ = TypeVar("_TJ")


def create_acr_db(to_eval: dict[str, _TJ], /) -> dict[int, AcrDb]:
    return {
        int(acr_id): from_dict(data_class=AcrDb, data=acr_db)
        for acr_id, acr_db in to_eval.items()
    }


_CAT_ACR: Final[Pattern[str]] = re.compile(r"\{acr\}")
_CAT_ID: Final[Pattern[str]] = re.compile(r"\{id\}")
_CAT_PRE: Final[Pattern[str]] = re.compile(r"\{pre\}")
_CAT_CORE: Final[Pattern[str]] = re.compile(r"\{core\}")
_CAT_SUF: Final[Pattern[str]] = re.compile(r"\{suf\}")

_OPT_VAL: Final[Pattern[str]] = re.compile(r"({[^{]+})?<.+?>({.+?})?")

_VALID_URI: Final[Pattern[str]] = re.compile(r"\{([^}]+?)\}")
_VALID_PAR: Final[set[str]] = {"acr", "id", "pre", "core", "suf"}


def check_uri_template(uri: str, /) -> None:
    for param in _VALID_URI.findall(uri):
        if param not in _VALID_PAR:
            raise ValJsonEx(f"invalid param name detected [{param}]")


_REPL_PARAM: Final[dict[str, Callable[[CatArgs], str]]] = {
    "{acr}": lambda cat: cat.acr,
    "{id}": lambda cat: cat.id,
    "{pre}": lambda cat: cat.pre,
    "{core}": lambda cat: cat.core,
    "{suf}": lambda cat: cat.suf,
}


def _rm_opt(href: str, left: str, right: str, /) -> str:
    return re.compile(re.escape(left) + r"<.+?>" + re.escape(right)).sub(
        f"{left}{right}", href, 1
    )


def _fix_opt(href: str, match: tuple[str, str], args: CatArgs, /) -> str:
    left, right = match
    if "" in [left, right]:
        return _rm_opt(href, left, right)
    left_f, right_f = _REPL_PARAM.get(left, None), _REPL_PARAM.get(right, None)
    if left_f is None or right_f is None:
        raise ValJsonEx(f"uri contains unknown parameter names - {href}")
    left_p, right_p = left_f(args), right_f(args)
    if "" in [left_p, right_p]:
        return _rm_opt(href, left, right)
    return re.compile(re.escape(left) + r"<(.+?)>" + re.escape(right)).sub(
        f"{left}\g<1>{right}", href, 1
    )


def replace_param_value(href: str, args: CatArgs, /) -> str:
    for opt in _OPT_VAL.findall(href):
        href = _fix_opt(href, opt, args)
    href = _CAT_ACR.sub(args.acr, href)
    href = _CAT_ID.sub(args.id, href)
    href = _CAT_PRE.sub(args.pre, href)
    href = _CAT_CORE.sub(args.core, href)
    return _CAT_SUF.sub(args.suf, href)
