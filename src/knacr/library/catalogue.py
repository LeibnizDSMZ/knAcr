from knacr.container.acr_db import AcrDb, CatArgs
from knacr.container.fun.acr_db import replace_param_value
from knacr.container.links import CatalogueLink, LinkLevel


def create_catalogue_link(acr_db: AcrDb, args: CatArgs, /) -> str:
    return replace_param_value(acr_db.catalogue, args)


def create_ccno_links(acr_db: AcrDb, args: CatArgs, /) -> CatalogueLink:
    if not acr_db.active or acr_db.deprecated:
        return CatalogueLink(level=LinkLevel.emp)
    cat_link = replace_param_value(acr_db.catalogue, args)
    hom_link = str(acr_db.homepage)
    match (cat_link, hom_link):
        case ("", ""):
            level = LinkLevel.emp
        case ("", _):
            level = LinkLevel.home
        case _:
            level = LinkLevel.cat
    return CatalogueLink(level=level, catalogue=cat_link, homepage=hom_link)
