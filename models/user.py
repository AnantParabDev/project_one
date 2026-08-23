from config.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from models.role import Role


class User(db.Model):
  __tablename__ = "users"
  user_id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100), nullable=False)
  email =db.Column(db.String(150), unique=True, nullable=False)
  password = db.Column(db.String(255), nullable=False)
  
  role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False, default=1)

  roles = db.relationship("Role", back_populates="users")


  def set_password(self, raw_password):
    self.password = generate_password_hash(raw_password)

  def check_password(self, raw_password):
    return check_password_hash(self.password, raw_password)

  def to_dict(self):
    return {
      "user_id" : self.user_id,
      "username" : self.username,
      "email" : self.email,
      "role_id" : self.role_id
    }