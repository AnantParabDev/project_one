from config.database import db
from models.category import Category

class CategoryService:
  def __init__(self, dao):
    self.category_dao = dao

  def add_category(self,category_name):
    category=Category(category_name = category_name)
    return self.category_dao.add_category(category)

  
  def get_all_category(self):
    return self.category_dao.get_all_category()

  def get_category_by_id(self, c_id):
    return self.category_dao.get_category_by_id(c_id)

  def update_category(self, category):
    return self.category_dao.update_category(category)

  def delete_category(self, c_id):
    category=self.category_dao.get_category_by_id(c_id)
    return self.category_dao.delete_category(category)
