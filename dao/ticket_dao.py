from config.database import db
from models.ticket import Ticket

class TicketDAO:

  def add_ticket(self, ticket):
    db.session.add(ticket)
    db.session.commit()
    return ticket

  def get_all_ticket(self, status=None, priority=None, assigned_to=None):
    query = Ticket.query  

    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if assigned_to:
        query = query.filter_by(assigned_to=assigned_to)

    return query.all()

  def get_ticket_by_id(self, t_id):
    return Ticket.query.get(t_id)

  def get_ticket_by_user_id(self, u_id):
    return Ticket.query.filter_by(user_id= u_id)

  def get_by_title(self, title):
    return Ticket.query.filter_by(title = title).first()

  def update_ticket(self, ticket):
    db.session.commit()
    return ticket

  def delete_ticket(self, ticket):
    db.session.delete(ticket)
    db.session.commit()
    return True