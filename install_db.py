from models import db, Guest
db.connect()
db.create_tables([Guest])