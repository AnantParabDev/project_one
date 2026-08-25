from config.database import db
from models.ticket_history import TicketHistory

class HistoryDAO:

    def add_history(self, ticket_history):
        db.session.add(ticket_history)
        db.session.commit()
        return ticket_history

    def get_history_by_ticket(self, ticket_id):
        return TicketHistory.query.filter_by(ticket_id=ticket_id).all()