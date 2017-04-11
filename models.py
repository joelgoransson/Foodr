from peewee import *
db = PostgresqlDatabase('webapp')
class Guest(Model):
	name = CharField()
	email = CharField()
	message = CharField()
	class Meta:
		database = db