import os
from peewee import PostgresqlDatabase, Model, CharField, BooleanField, ForeignKeyField, TextField
from flask_security import UserMixin, RoleMixin
from playhouse.db_url import connect

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    db = connect(DATABASE_URL)
else:
    DATABASE = 'webapp'
    db = PostgresqlDatabase(DATABASE)

class BaseModel(Model):
	class Meta:
		database = db

class Food(BaseModel):
	name = CharField(unique=True)

class User(BaseModel, UserMixin):
	picture = CharField(default="/static/profile_pic.png")
	username = CharField(unique=True)
	about_me = TextField(default="")
	email = CharField(unique=True)
	password = CharField()
	active = BooleanField(default=True)
	favorite_food = ForeignKeyField(Food, null=True, default=None)

class Image(BaseModel):
	user = ForeignKeyField(User)
	url = CharField()

class Post(BaseModel):
	user = ForeignKeyField(User)
	text = CharField()

class Role(BaseModel, RoleMixin):
    name = CharField(unique=True)
    description = CharField(null=True)

class UserRoles(BaseModel):
    user = ForeignKeyField(User, related_name="roles")
    role = ForeignKeyField(User, related_name="users")
    name = property(lambda self: self.role.name)
    description = property(lambda self: self.role.description)
