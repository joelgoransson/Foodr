import getpass
from models import db, Food
from flask_security import PeeweeUserDatastore
from models import db, User, Role, UserRoles

user_datastore = PeeweeUserDatastore(db, User, Role, UserRoles)
def create_user(email, username, password=None):
    about_me = ''
    favorite_food=''

    if password is None:
        password = getpass.getpass()
    user_datastore.create_user(email=email, about_me=about_me, password=password, username=username)