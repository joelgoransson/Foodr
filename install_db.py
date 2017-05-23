from models import db, User, Role, UserRoles, Food, Image
db.connect()
db.create_tables([Food, User, Role, UserRoles, Image], safe=True)