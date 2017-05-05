import getpass

from app import user_datastore
from models import db, Food

def create_user(email, favorite_food, password=None):
    food = Food.select().where(Food.name == favorite_food)
    if len(food) == 0:
    	food = Food(name=favorite_food)
    	food.save()
    else:
    	food = food[0]

    if password is None:
        password = getpass.getpass()
    user_datastore.create_user(email=email, password=password, favorite_food=food)