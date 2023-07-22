from knacr.container.fun.acr_db import get_brc_merge_type


ACR_DB = {
    "type": "object",
    "patternProperties": {"^[1-9][0-9]*$": {"$ref": "#/definitions/AcrCon"}},
    "additionalProperties": False,
    "required": [],
    "definitions": {
        "AcrCon": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "minLength": 2, "pattern": "^[A-Z:]+$"},
                "acr": {"type": "string", "minLength": 2, "pattern": "^[A-Z:]+$"},
                "acr_synonym": {
                    "type": "array",
                    "items": {"type": "string", "minLength": 2, "pattern": "^[A-Z:]+$"},
                    "minLength": 1,
                },
                "acr_changed_to": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer", "minimum": 1},
                            "type": {"type": "string", "enum": get_brc_merge_type()},
                        },
                    },
                    "minLength": 1,
                },
                "name": {"type": "string", "minLength": 2},
                "country": {"type": "string", "pattern": "^[A-Z]{2}$"},
                "active": {"type": "boolean"},
                "deprecated": {"type": "boolean"},
                "homepage": {"type": "string", "pattern": "^http.*$", "format": "uri"},
                "catalogue": {
                    "type": "string",
                    "pattern": "^http.*$",
                    "format": "uri-template",
                },
                "regex_ccno": {"type": "string", "format": "regex", "minLength": 4},
                "regex_id": {"type": "string", "format": "regex", "minLength": 4},
            },
            "required": [
                "code",
                "acr",
                "name",
                "active",
                "country",
                "regex_ccno",
                "regex_id",
            ],
            "additionalProperties": False,
        }
    },
}


ACR_MIN_DB = {
    "type": "object",
    "patternProperties": {"^[1-9][0-9]*$": {"$ref": "#/definitions/AcrCon"}},
    "additionalProperties": False,
    "required": [],
    "definitions": {
        "AcrCon": {
            "type": "object",
            "properties": {
                "acr": {"type": "string", "minLength": 2, "pattern": "^[A-Z:]+$"},
                "deprecated": {"type": "boolean"},
            },
            "required": ["acr"],
            "additionalProperties": True,
        }
    },
}
