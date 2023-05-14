from knacr.container.acr_db import AcrDb, CatArgs
from knacr.container.fun.acr_db import replace_param_value


def create_catalogue_link(acr_db: AcrDb, args: CatArgs, /) -> str:
    return replace_param_value(acr_db.catalogue, args)
