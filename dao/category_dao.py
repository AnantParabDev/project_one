from config.database import db
from models.category import Category

class CategoryDAO:

  def add_category(self, category):
    db.session.add(category)
    db.session.commit()
    return category

  def get_all_category(self):
    return Category.query.all()

  def get_category_by_id(self, c_id):
    return Category.query.get(c_id)

  def update_category(self, category):
    db.session.commit()
    return category

  def delete_category(self, category):
    db.session.delete(category)
    db.session.commit()
    return True