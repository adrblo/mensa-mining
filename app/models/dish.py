from app.database import Base
from sqlalchemy import Column, Integer, String, Text, Float, Date, ForeignKey
from sqlalchemy.orm import relationship


class Dish(Base):
    __tablename__ = 'dish'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    name_de = Column(String)
    description_de = Column(Text)
    category = Column(String)
    category_de = Column(String)
    subcategory_de = Column(String)
    priceStudents = Column(Float)
    priceWorkers = Column(Float)
    priceGuests = Column(Float)
    order_info = Column(Integer)
    restaurant = Column(String)
    pricetype = Column(String)
    image = Column(String)
    thumbnail = Column(String)

    allergens = relationship("Allergen", back_populates="dish")
    badges = relationship("Badge", back_populates="dish")


class Allergen(Base):
    __tablename__ = 'allergen'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    dish_id = Column(Integer, ForeignKey('dish.id'))

    dish = relationship("Dish", back_populates="allergens")


class Badge(Base):
    __tablename__ = 'badge'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    dish_id = Column(Integer, ForeignKey('dish.id'))

    dish = relationship("Dish", back_populates="badges")
