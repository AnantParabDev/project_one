from config.database import db
from datetime import datetime

class TicketHistory(db.Model):
    __tablename__ = 'ticket_history'
    history_id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.ticket_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    old_value = db.Column(db.String(255), nullable=True)
    new_value = db.Column(db.String(255), nullable=True)
    changed_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {'history_id': self.history_id, 'ticket_id': self.ticket_id, 'user_id': self.user_id, 'action': self.action, 'old_value': self.old_value, 'new_value': self.new_value, 'changed_at': self.changed_at}