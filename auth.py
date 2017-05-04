import getpass

from app import user_datastore
from models import db

def create_user(email, password=None):
    if password is None:
        password = getpass.getpass()
    user_datastore.create_user(email=email, password=password)