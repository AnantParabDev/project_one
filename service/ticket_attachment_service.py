from config.database import db
from models.ticket_attachment import TicketAttachment

class TicketAttachmentService:

    def __init__(self, dao):
        self.ticket_attachment_dao = dao

    def add_ticket_attachment(self, file_name, file_path, ticket_id, uploaded_by):
        attachment = TicketAttachment(file_name=file_name, file_path=file_path, ticket_id=ticket_id, uploaded_by=uploaded_by)
        return self.ticket_attachment_dao.add_ticket_attachment(attachment)

    def get_all_ticket_attachment(self):
        return self.ticket_attachment_dao.get_all_ticket_attachment()

    def get_by_title(self, title):
        return self.ticket_attachment_dao.get_by_title(title)

    def get_ticket_attachment_by_id(self, t_id):
        return self.ticket_attachment_dao.get_ticket_attachment_by_id(t_id)

    def get_ticket_attachment_by_ticket_id(self, t_id):
        return self.ticket_attachment_dao.get_ticket_attachment_by_ticket_id(t_id)

    def get_ticket_attachment_by_user_id(self, u_id):
        return self.ticket_attachment_dao.get_ticket_attachment_by_user_id(u_id)

    def update_ticket_attachment(self, ticket_attachment):
        return self.ticket_attachment_dao.update_ticket_attachment(ticket_attachment)

    def delete_ticket_attachment(self, ticket_attachment):
        return self.ticket_attachment_dao.delete_ticket_attachment(ticket_attachment)