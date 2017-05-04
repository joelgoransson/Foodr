import os
from peewee import PostgresqlDatabase, Model, CharField, BooleanField, ForeignKeyField
from flask_security import UserMixin, RoleMixin
from playhouse.db_url import connect

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    db = connect(DATABASE_URL)
else:
    DATABASE = 'webapp'
    db = PostgresqlDatabase(DATABASE)

class Guest(Model):
	name = CharField()
	username = CharField()
	email = CharField()
	message = CharField()
	class Meta:
		database = db

class BaseModel(Model):
	class Meta:
		database = db

class User(BaseModel, UserMixin):
    email = CharField(unique=True)
    password = CharField()
    active = BooleanField(default=True)

class Role(BaseModel, RoleMixin):
    name = CharField(unique=True)
    description = CharField(null=True)

class UserRoles(BaseModel):
    user = ForeignKeyField(User, related_name="roles")
    role = ForeignKeyField(User, related_name="users")
    name = property(lambda self: self.role.name)
    description = property(lambda self: self.role.description)
