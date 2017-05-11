import getpass

from app import user_datastore
from models import db, Food

def create_user(email, favorite_food, name, username, password=None):
    food = Food.select().where(Food.name == favorite_food)
    about_me = ''
    if len(food) == 0:
    	food = Food(name=favorite_food)
    	food.save()
    else:
    	food = food[0]

    if password is None:
        password = getpass.getpass()
    user_datastore.create_user(email=email,name=name, about_me=about_me, password=password, username=username, favorite_food=food)