import os
from peewee import PostgresqlDatabase, Model, CharField
from playhouse.db_url import connect

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    db = connect(DATABASE_URL)
else:
    DATABASE = 'webapp'
    db = PostgresqlDatabase(DATABASE)

class Guest(Model):
	name = CharField()
	email = CharField()
	message = CharField()
	class Meta:
		database = db