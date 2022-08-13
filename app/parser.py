import json
import requests

from app.core.config import settings
from app.database import Base
from app.database.session import engine, SessionLocal
from app import schemas


def get_mensa_api_response():
    return requests.get(settings.API_URL).json()


def save_dict_to_json(filename, data):
    """
    Save a dictionary to a json file.
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def map_dish_schema_to_model(dish_list: schemas.DishList):
    db_dishes = []

    for dish in dish_list.dishes:
        db_allergens = []
        db_badges = []

        # map schema dish to model dish
        db_dish = models.Dish(
            date=dish.date,
            name_de=dish.name_de,
            description_de=dish.description_de,
            category=dish.category,
            category_de=dish.category_de,
            subcategory_de=dish.subcategory_de,
            priceStudents=dish.priceStudents,
            priceWorkers=dish.priceWorkers,
            priceGuests=dish.priceGuests,
            order_info=dish.order_info,
            restaurant=dish.restaurant,
            pricetype=dish.pricetype,
            image=dish.image,
            thumbnail=dish.thumbnail
        )

        for allergen in dish.allergens:
            db_allergens.append(models.Allergen(name=allergen))

        for badge in dish.badges:
            db_badges.append(models.Badge(name=badge))

        db_dishes.append((db_dish, db_allergens, db_badges))

    return db_dishes


if __name__ == "__main__":
    from app import models

    session = SessionLocal()

    Base.metadata.create_all(engine)

    db_dishes = map_dish_schema_to_model(schemas.DishList(dishes=get_mensa_api_response()))

    # remove duplicates
    for dish, allergens, badges in db_dishes:
        if not session.query(models.Dish).filter_by(name_de=dish.name_de, date=dish.date).first():
            session.add(dish)
            session.commit()

            session.refresh(dish)

            for allergen in allergens:
                allergen.dish_id = dish.id
                session.add(allergen)

            for badge in badges:
                badge.dish_id = dish.id
                session.add(badge)

            session.commit()

    session.commit()

    session.close()


