from models import db, Contact
db.connect()
db.create_tables([Contact])