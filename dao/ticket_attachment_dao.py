from config.database import db
from models.ticket_attachment import TicketAttachment

class TicketAttachmentDAO:

    def add_ticket_attachment(self, ticket_attachment):
        db.session.add(ticket_attachment)
        db.session.commit()
        return ticket_attachment

    def get_all_ticket_attachment(self):
        return TicketAttachment.query.all()

    def get_ticket_attachment_by_id(self, t_id):
        return TicketAttachment.query.get(t_id)

    def get_ticket_attachment_by_ticket_id(self, t_id):
        return TicketAttachment.query.filter_by(ticket_id=t_id).all()

    def get_ticket_attachment_by_user_id(self, u_id):
        return TicketAttachment.query.filter_by(uploaded_by=u_id).all()

    def get_by_title(self, title):
        return TicketAttachment.query.filter_by(title=title).first()

    def update_ticket_attachment(self, ticket_attachment):
        db.session.commit()
        return ticket_attachment

    def delete_ticket_attachment(self, ticket_attachment):
        db.session.delete(ticket_attachment)
        db.session.commit()
        return True