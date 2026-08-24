from config.database import db

class Category(db.Model):
  __tablename__ = "categories"
  category_id = db.Column(db.Integer, primary_key=True)
  category_name = db.Column(db.String(25), nullable=False)

  tickets = db.relationship("Ticket", back_populates="category")


  def to_dict(self):
    return {
      "category_id" : self.category_id,
      "category_name" : self.category_name
    }