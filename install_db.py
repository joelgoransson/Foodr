from models import db, User, Role, UserRoles
db.connect()
db.create_tables([User, Role, UserRoles], safe=True)