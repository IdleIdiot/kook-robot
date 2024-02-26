import json


def json_load(config_path: str) -> dict:
    with open(config_path) as f:
        return json.load(f)
