from config.database import db
from models.user import User

class UserService:

    def __init__(self, dao):
        self.user_dao = dao

    def add_user(self, username, email, password, role_id):
        user = User(username=username, email=email, role_id=role_id)
        user.set_password(password)
        return self.user_dao.add_user(user)

    def get_all_user(self):
        return self.user_dao.get_all_user()

    def get_by_username(self, name):
        return self.user_dao.get_by_username(name)

    def get_user_by_email(self, email):
        return self.user_dao.get_user_by_email(email)

    def get_user_by_id(self, u_id):
        return self.user_dao.get_user_by_id(u_id)

    def update_user(self, user):
        return self.user_dao.update_user(user)

    def delete_user(self, u_id):
        user = self.user_dao.get_user_by_id(u_id)
        return self.user_dao.delete_user(user)

    def verify_login(self, email, password):
        user = self.get_user_by_email(email)
        if user and user.check_password(password):
            return user
        return None