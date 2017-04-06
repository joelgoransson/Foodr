from peewee import *
db = SqliteDatabase('guest.db')
class Guest(Model):
	name = CharField()
	email = CharField()
	message = CharField()
	class Meta:
		database = db