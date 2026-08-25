from flask import jsonify, Blueprint
from flask_jwt_extended import get_jwt, jwt_required
from dao.ticket_dao import TicketDAO
from service import ticket_service
from service.ticket_service import TicketService
dashboard_bp = Blueprint('dashboard', __name__)
ticket_service = TicketService(TicketDAO())

@dashboard_bp.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def view_dashboard_stats():
    claims = get_jwt()
    if claims.get('role') != 'ADMIN':
        return (jsonify({'message': 'Only Admins can view the dashboard'}), 403)
    stats = ticket_service.get_dashboard_stats()
    return (jsonify({'message': 'Dashboard Statistics', 'statistics': stats}), 200)