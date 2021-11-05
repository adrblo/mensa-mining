import datetime
import json
from typing import Optional, List

from pydantic import BaseModel

import requests


class Dish(BaseModel):
    date: datetime.date
    name_de: str
    description_de: str
    category: str
    category_de: str
    subcategory_de: str
    priceStudents: float
    priceWorkers: float
    priceGuests: float
    allergens: List[str] = []
    order_info: int
    badges: List[str] = []
    restaurant: str
    pricetype: str
    image: str
    thumbnail: str

    def __hash__(self):
        return hash(self.json())


class DishList(BaseModel):
    dishes: List[Dish]


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
