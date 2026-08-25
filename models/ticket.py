from config.database import db
from datetime import datetime

class Ticket(db.Model):
    __tablename__ = 'tickets'
    ticket_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    status = db.Column(db.String(25), nullable=False, default='open')
    priority = db.Column(db.String(25), nullable=False, default='Low')
    created_at = db.Column(db.DateTime, default=datetime.now)
    due_date = db.Column(db.DateTime, nullable=True)
    category = db.relationship('Category', back_populates='tickets')

    def to_dict(self):
        return {'ticket_id': self.ticket_id, 'title': self.title, 'description': self.description, 'category_id': self.category_id, 'created_by': self.created_by, 'assigned_to': self.assigned_to, 'status': self.status, 'priority': self.priority, 'created_at': self.created_at.isoformat() if self.created_at else None, 'due_date': self.due_date.isoformat() if self.due_date else None}