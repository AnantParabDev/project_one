from dao.history_dao import HistoryDAO
from models.ticket_history import TicketHistory

class HistoryService:

    def __init__(self, dao):
        self.history_dao = dao

    def add_history(self, ticket_id, user_id, action, old_value, new_value):
        history_dao = TicketHistory(ticket_id=ticket_id, user_id=user_id, action=action, old_value=old_value, new_value=new_value)
        return self.history_dao.add_history(history_dao)

    def get_history_by_ticket(self, ticket_id):
        return self.history_dao.get_history_by_ticket(ticket_id)