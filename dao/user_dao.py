from config.database import db
from models.user import User

class UserDAO:

    def add_user(self, user):
        db.session.add(user)
        db.session.commit()
        return user

    def get_all_user(self):
        return User.query.all()

    def get_by_username(self, name):
        return User.query.filter_by(username=name).first()

    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def get_user_by_id(self, u_id):
        return User.query.get(u_id)

    def update_user(self, user):
        db.session.commit()
        return user

    def delete_user(self, user):
        db.session.delete(user)
        db.session.commit()
        return True