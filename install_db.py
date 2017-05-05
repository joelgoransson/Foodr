from models import db, User, Role, UserRoles, Food
db.connect()
db.create_tables([Food, User, Role, UserRoles], safe=True)