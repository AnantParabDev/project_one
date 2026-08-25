from app import create_app
from config.database import db
from models.role import Role
from models.category import Category
from models.user import User
app = create_app()
with app.app_context():
    roles = [Role(role_id=1, roles='USER'), Role(role_id=2, roles='SUPPORT_AGENT'), Role(role_id=3, roles='ADMIN')]
    for r in roles:
        if not Role.query.get(r.role_id):
            db.session.add(r)
    categories = [Category(category_id=1, category_name='Hardware'), Category(category_id=2, category_name='Software'), Category(category_id=3, category_name='Network'), Category(category_id=4, category_name='Access/Login')]
    for c in categories:
        if not Category.query.get(c.category_id):
            db.session.add(c)
    db.session.commit()
    users = [{'username': 'superadmin', 'email': 'admin@servicedesk.com', 'password': 'password123', 'role_id': 3}, {'username': 'tech_dave', 'email': 'dave@servicedesk.com', 'password': 'password123', 'role_id': 2}, {'username': 'bob_sales', 'email': 'bob@company.com', 'password': 'password123', 'role_id': 1}]
    for u_data in users:
        if not User.query.filter_by(email=u_data['email']).first():
            new_user = User(username=u_data['username'], email=u_data['email'], role_id=u_data['role_id'])
            new_user.set_password(u_data['password'])
            db.session.add(new_user)
    db.session.commit()
    print('Database seeded successfully.')