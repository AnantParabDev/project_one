from config.database import db
from datetime import datetime

class Comment(db.Model):
  __tablename__ = "ticket_comments"
  comment_id = db.Column(db.Integer, primary_key=True)
  comment = db.Column(db.Text, nullable=False)

  ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.ticket_id'), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

  created_at = db.Column(db.DateTime, default=datetime.now) 


  def to_dict(self):
    return {
      "comment_id" :self.comment_id,
      "comment" : self.comment,

      "ticket_id" : self.ticket_id,
      "user_id" : self.user_id,

      "created_at" : self.created_at
    }
    