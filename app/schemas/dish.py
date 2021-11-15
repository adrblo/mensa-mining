import datetime
from typing import List

from pydantic import BaseModel


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
