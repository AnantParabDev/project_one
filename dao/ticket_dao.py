"""
ticket_dao.py
-------------
Data Access Object for all database operations on the Ticket model.
Provides clean, reusable methods so the service layer never touches
the SQLAlchemy session directly.

Author: Anant Parab
"""

from config.database import db
from models.ticket import Ticket


class TicketDAO:

    def add_ticket(self, ticket):
        """Persist a new Ticket object and return it with its generated ID."""
        db.session.add(ticket)
        db.session.commit()
        return ticket

    def get_all_ticket(self, status=None, priority=None, assigned_to=None):
        """
        Return all tickets, optionally filtered by status, priority,
        or the ID of the agent they are assigned to.
        """
        query = Ticket.query

        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)
        if assigned_to:
            query = query.filter_by(assigned_to=assigned_to)

        return query.all()

    def get_ticket_by_id(self, t_id):
        """Return a single Ticket by its primary key, or None."""
        return Ticket.query.get(t_id)

    def get_ticket_by_user_id(self, u_id):
        """
        Return all tickets created by a particular user.
        Uses the 'created_by' foreign key column (not 'user_id').
        """
        return Ticket.query.filter_by(created_by=u_id).all()

    def get_by_title(self, title):
        """Return the first ticket whose title matches exactly."""
        return Ticket.query.filter_by(title=title).first()

    def update_ticket(self, ticket):
        """Flush the current session to save any in-memory changes to the DB."""
        db.session.commit()
        return ticket

    def delete_ticket(self, ticket):
        """Delete a ticket record from the database."""
        db.session.delete(ticket)
        db.session.commit()
        return True

                                                                        
                                    
                                                                        

    def get_total_tickets_count(self):
        """Return the total number of tickets in the system."""
        return Ticket.query.count()

    def get_count_by_status(self, status_name):
        """Return the number of tickets with the given status string."""
        return Ticket.query.filter_by(status=status_name).count()

    def get_unassigned_count(self):
        """Return the number of tickets that have not been assigned yet."""
        return Ticket.query.filter_by(assigned_to=None).count()