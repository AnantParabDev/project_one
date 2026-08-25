from config.database import db
from dao.history_dao import HistoryDAO
from models.ticket import Ticket
from service import history_service
from service.history_service import HistoryService
from models.ticket_history import TicketHistory
history_service = HistoryService(HistoryDAO())

class TicketService:

    def __init__(self, dao):
        self.ticket_dao = dao

    def add_ticket(self, title, description, category_id, created_by, priority):
        from datetime import datetime, timedelta
        due_date = None
        if priority and priority.lower() == 'high':
            due_date = datetime.now() + timedelta(days=1)
        elif priority and priority.lower() == 'medium':
            due_date = datetime.now() + timedelta(days=3)
        else:
            due_date = datetime.now() + timedelta(days=7)
        ticket = Ticket(title=title, description=description, category_id=category_id, created_by=created_by, priority=priority, due_date=due_date)
        return self.ticket_dao.add_ticket(ticket)

    def get_all_ticket(self, status=None, priority=None, assigned_to=None):
        return self.ticket_dao.get_all_ticket(status, priority, assigned_to)

    def get_by_title(self, title):
        return self.ticket_dao.get_by_title(title)

    def get_ticket_by_id(self, t_id):
        return self.ticket_dao.get_ticket_by_id(t_id)

    def get_ticket_by_user_id(self, u_id):
        return self.ticket_dao.get_ticket_by_user_id(u_id)

    def update_ticket(self, ticket):
        return self.ticket_dao.update_ticket(ticket)

    def update_ticket_assignment(self, t_id, agent_id):
        ticket = self.get_ticket_by_id(t_id)
        setattr(ticket, 'assigned_to', agent_id)
        return self.ticket_dao.update_ticket(ticket)

    def update_ticket_status(self, t_id, new_status, current_user_id):
        ticket = self.get_ticket_by_id(t_id)
        old_status = ticket.status
        ticket.status = new_status
        self.ticket_dao.update_ticket(ticket)
        history_service.add_history(ticket_id=t_id, user_id=current_user_id, action='Status Changed', old_value=old_status, new_value=new_status)
        return ticket

    def update_ticket_priority(self, t_id, priority):
        ticket = self.get_ticket_by_id(t_id)
        setattr(ticket, 'priority', priority)
        return self.ticket_dao.update_ticket(ticket)

    def delete_ticket(self, u_id):
        ticket = self.ticket_dao.get_ticket_by_id(u_id)
        return self.ticket_dao.delete_ticket(ticket)

    def get_dashboard_stats(self):
        stats = {'total_tickets': self.ticket_dao.get_total_tickets_count(), 'open_tickets': self.ticket_dao.get_count_by_status('open'), 'resolved_tickets': self.ticket_dao.get_count_by_status('resolved'), 'unassigned_tickets': self.ticket_dao.get_unassigned_count()}
        return stats