from config.database import db
from datetime import datetime

class TicketAttachment(db.Model):
    __tablename__ = 'ticket_attachments'
    attachment_id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.ticket_id'), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {'ticket_id': self.ticket_id, 'attachment_id': self.attachment_id, 'file_name': self.file_name, 'file_path': self.file_path, 'uploaded_by': self.uploaded_by, 'uploaded_at': self.uploaded_at if self.uploaded_at else None}