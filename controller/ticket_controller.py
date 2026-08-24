from flask import request, Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt

from dao.ticket_dao import TicketDAO
from service.ticket_service import TicketService

ticket_service = TicketService(TicketDAO())

ticket_bp = Blueprint("ticket", __name__)

@ticket_bp.route('/api/tickets', methods=['POST', 'GET'])
@jwt_required()
def add_tickets():
  if request.method == 'GET':
    status_filter = request.args.get('status')
    priority_filter = request.args.get('priority')
    assigned_to_filter = request.args.get('assigned_to_filter')

    tickets = ticket_service.get_all_ticket(status_filter, priority_filter, assigned_to_filter)
    
    ticket_list = [t.to_dict() for t in tickets]
    return jsonify(ticket_list), 200
  else:
    data = request.get_json()

    title = data.get('title')
    description = data.get("description")
    category_id = data.get("category_id")
    current_user_id = get_jwt_identity()
    priority = data.get("priority")

    ticket = ticket_service.add_ticket(title, description, category_id, current_user_id, priority)

    return jsonify(
        {
            "message": "Ticket Created Successfully",
            "ticket": ticket.to_dict()
        }
    ), 201


@ticket_bp.route('/api/tickets/<int:t_id>', methods=['GET'])
def view_single_ticket(t_id):
  ticket = ticket_service.get_ticket_by_id(t_id)
  if ticket:
    return jsonify(ticket.to_dict()), 200
  return jsonify(
      {
          "message": "Invalid Ticket ID"
      }
  ), 404

  
@ticket_bp.route('/api/tickets/<int:t_id>/assign', methods=['PUT'])
@jwt_required()
def assign_ticket(t_id):

  claims = get_jwt()
  print(claims.get('role'))
  if claims.get('role') != 'ADMIN':
    return jsonify({
      "message"  : "Only Admins can assign Tickets"
    }), 403

  data = request.get_json()
  agent_id = data.get("assigned_to")

  ticket = ticket_service.update_ticket_assignment(t_id, agent_id)
  
  if ticket:
    return jsonify({
      "message" : "Ticket Assigned",
      "ticket" :ticket.to_dict()}), 200
  return jsonify(
      {
          "message": "Invalid Ticket ID"
      }
  ), 404

@ticket_bp.route('/api/tickets/<int:t_id>/status', methods=['PUT'])
@jwt_required()
def modify_status(t_id):

  claims = get_jwt()
  # print(claims.get('role'))
  role = claims.get('role')
  if role not in ['ADMIN', 'SUPPORT_AGENT']:
    return jsonify({
      "message"  : "Only Admins or Support agent can modify ticket status"
    }), 403

  data = request.get_json()
  status = data.get("status")

  ticket = ticket_service.update_ticket_status(t_id, status)
  
  if ticket:
    return jsonify({
      "message" : "Status Modified",
      "ticket" :ticket.to_dict()}), 200
  return jsonify(
      {
          "message": "Invalid Ticket ID"
      }
  ), 404

@ticket_bp.route('/api/tickets/<int:t_id>/priority', methods=['PUT'])
@jwt_required()
def modify_priority(t_id):

  claims = get_jwt()
  # print(claims.get('role'))
  role = claims.get('role')
  if role not in ['ADMIN', 'SUPPORT_AGENT']:
    return jsonify({
      "message"  : "Only Admins or Support agent can escalate tickets"
    }), 403

  data = request.get_json()
  priority = data.get("priority")

  ticket = ticket_service.update_ticket_priority(t_id, priority)
  
  if ticket:
    return jsonify({
      "message" : "Priority Modified",
      "ticket" :ticket.to_dict()}), 200
  return jsonify(
      {
          "message": "Invalid Ticket ID"
      }
  ), 404