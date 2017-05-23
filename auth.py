import getpass

from app import user_datastore
from models import db, Food

def create_user(email, username, password=None):
    about_me = ''
    favorite_food=''

    if password is None:
        password = getpass.getpass()
    user_datastore.create_user(email=email, about_me=about_me, password=password, username=username)