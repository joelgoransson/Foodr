from peewee import *
db = SqliteDatabase('contact.db')
class Contact(Model):
	name = CharField()
	email = CharField()
	message = CharField()
	class Meta:
		database = db
	