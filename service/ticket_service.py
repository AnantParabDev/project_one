from config.database import db
from dao import ticket_dao
from models.ticket import Ticket

# from dao.ticket_dao import TicketDAO


class TicketService:
  def __init__(self, dao):
    self.ticket_dao = dao

  def add_ticket(self, title, description, category_id, created_by, priority):
    ticket=Ticket(title=title, description=description, category_id=category_id, created_by=created_by, priority=priority)
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

  def update_ticket_status(self, t_id, status):
    ticket = self.get_ticket_by_id(t_id)
    setattr(ticket, 'status', status)
    return self.ticket_dao.update_ticket(ticket)

  def update_ticket_priority(self, t_id, priority):
    ticket = self.get_ticket_by_id(t_id)
    setattr(ticket, 'priority', priority)
    return self.ticket_dao.update_ticket(ticket)

  def delete_ticket(self, u_id):
    ticket=self.ticket_dao.get_ticket_by_id(u_id)
    return self.ticket_dao.delete_ticket(ticket)