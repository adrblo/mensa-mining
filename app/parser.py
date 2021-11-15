import datetime
import json
from typing import Optional, List

from pydantic import BaseModel

import requests



def get_mensa_api_response():
    return requests.get('')


def save_dict_to_json(filename, data):
    """
    Save a dictionary to a json file.
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    res = get_mensa_api_response()
    loaded_json = res.json()
    dishes = DishList(dishes=loaded_json).dishes
    print(dishes)
