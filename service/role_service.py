from config.database import db
from models.role import Role

class RoleService:
  def __init__(self, dao):
    self.role_dao = dao

  def add_role(self,roles):
    role=Role(roles=roles)
    return self.role_dao.add_role(role)

  
  def get_all_role(self):
    return self.role_dao.get_all_role()

  def get_role_by_id(self, r_id):
    return self.role_dao.get_role_by_id(r_id)

  def update_role(self, role):
    return self.role_dao.update_role(role)

  def delete_role(self, u_id):
    role=self.role_dao.get_role_by_id(u_id)
    return self.role_dao.delete_role(role)
