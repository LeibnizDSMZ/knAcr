from knacr.container.fun.acr_db import get_brc_merge_type


ACR_DB = {
    "type": "object",
    "properties": {
        "patternProperties": {"^[1-9][0-9]*$": {"$ref": "#/definitions/AcrCon"}},
        "additionalProperties": False,
    },
    "required": [],
    "definitions": {
        "AcrCon": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "minLength": 2},
                "acr": {"type": "string", "minLength": 2},
                "acr_syn": {
                    "type": "array",
                    "items": {"type": "string", "minLength": 2},
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
                },
                "name": {"type": "string", "minLength": 2},
                "active": {"type": "boolean"},
                "homepage": {"type": "string", "format": "uri"},
                "catalogue": {"type": "string", "format": "uri-template"},
                "regex_ccno": {"type": "string", "format": "regex"},
                "regex_id": {"type": "string", "format": "regex"},
            },
            "required": ["code", "acr", "name", "active", "regex_ccno", "regex_id"],
            "additionalProperties": False,
        }
    },
}
