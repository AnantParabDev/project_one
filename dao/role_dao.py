from config.database import db
from models.role import Role

class RoleDAO:

    def add_role(self, role):
        db.session.add(role)
        db.session.commit()
        return role

    def get_by_role(self, role):
        return Role.query.filter_by(role=role).first()

    def get_role_by_id(self, r_id):
        return Role.query.get(r_id)

    def update_role(self, role):
        db.session.commit()
        return role

    def delete_role(self, role):
        db.session.delete(role)
        db.session.commit()
        return True