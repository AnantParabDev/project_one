import os
from flask import Blueprint, current_app, jsonify, redirect, render_template, request, send_from_directory
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from werkzeug.utils import secure_filename
from dao.category_dao import CategoryDAO
from dao.comment_dao import CommentDAO
from dao.user_dao import UserDAO
from dao.history_dao import HistoryDAO
from dao.ticket_dao import TicketDAO
from service.category_service import CategoryService
from service.comment_service import CommentService
from service.user_service import UserService
from service.history_service import HistoryService
from service.ticket_attachment_service import TicketAttachmentService
from service.ticket_service import TicketService
from dao.ticket_attachment_dao import TicketAttachmentDAO
ticket_service = TicketService(TicketDAO())
category_service = CategoryService(CategoryDAO())
comment_service = CommentService(CommentDAO())
user_service = UserService(UserDAO())
ticket_attachment_service = TicketAttachmentService(TicketAttachmentDAO())
history_service = HistoryService(HistoryDAO())
ticket_bp = Blueprint('ticket', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    if '.' in filename:
        extension = filename.rsplit('.', 1)[1].lower()
        return extension in ALLOWED_EXTENSIONS
    return False

@ticket_bp.route('/api/tickets', methods=['GET', 'POST'])
@jwt_required()
def api_tickets():
    if request.method == 'GET':
        status_filter = request.args.get('status')
        priority_filter = request.args.get('priority')
        assigned_to_filter = request.args.get('assigned_to_filter')
        tickets = ticket_service.get_all_ticket(status_filter, priority_filter, assigned_to_filter)
        ticket_list = [t.to_dict() for t in tickets]
        return (jsonify(ticket_list), 200)
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    category_id = data.get('category_id')
    priority = data.get('priority')
    current_user_id = get_jwt_identity()
    ticket = ticket_service.add_ticket(title, description, category_id, current_user_id, priority)
    return (jsonify({'message': 'Ticket Created Successfully', 'ticket': ticket.to_dict()}), 201)

@ticket_bp.route('/api/tickets/<int:t_id>', methods=['GET'])
def api_view_single_ticket(t_id):
    ticket = ticket_service.get_ticket_by_id(t_id)
    if ticket:
        return (jsonify(ticket.to_dict()), 200)
    return (jsonify({'message': 'Invalid Ticket ID'}), 404)

@ticket_bp.route('/api/tickets/<int:t_id>/assign', methods=['PUT'])
@jwt_required()
def api_assign_ticket(t_id):
    claims = get_jwt()
    if claims.get('role') != 'ADMIN':
        return (jsonify({'message': 'Only Admins can assign Tickets'}), 403)
    data = request.get_json()
    agent_id = data.get('assigned_to')
    ticket = ticket_service.update_ticket_assignment(t_id, agent_id)
    if ticket:
        return (jsonify({'message': 'Ticket Assigned', 'ticket': ticket.to_dict()}), 200)
    return (jsonify({'message': 'Invalid Ticket ID'}), 404)

@ticket_bp.route('/api/tickets/<int:t_id>/status', methods=['PUT'])
@jwt_required()
def api_modify_status(t_id):
    claims = get_jwt()
    role = claims.get('role')
    if role not in ['ADMIN', 'SUPPORT_AGENT']:
        return (jsonify({'message': 'Only Admins or Support Agents can modify ticket status'}), 403)
    data = request.get_json()
    status = data.get('status')
    user_id = get_jwt_identity()
    ticket = ticket_service.update_ticket_status(t_id, status, user_id)
    if ticket:
        return (jsonify({'message': 'Status Modified', 'ticket': ticket.to_dict()}), 200)
    return (jsonify({'message': 'Invalid Ticket ID'}), 404)

@ticket_bp.route('/api/tickets/<int:t_id>/priority', methods=['PUT'])
@jwt_required()
def api_modify_priority(t_id):
    claims = get_jwt()
    role = claims.get('role')
    if role not in ['ADMIN', 'SUPPORT_AGENT']:
        return (jsonify({'message': 'Only Admins or Support Agents can escalate tickets'}), 403)
    data = request.get_json()
    priority = data.get('priority')
    ticket = ticket_service.update_ticket_priority(t_id, priority)
    if ticket:
        return (jsonify({'message': 'Priority Modified', 'ticket': ticket.to_dict()}), 200)
    return (jsonify({'message': 'Invalid Ticket ID'}), 404)

@ticket_bp.route('/api/tickets/<int:t_id>/attachments', methods=['POST'])
@jwt_required()
def api_upload_file(t_id):
    if 'file' not in request.files:
        return (jsonify({'message': 'File part not found'}), 400)
    file = request.files['file']
    if file.filename == '':
        return (jsonify({'message': 'File not selected'}), 400)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        uploaded_by = get_jwt_identity()
        attachment = ticket_attachment_service.add_ticket_attachment(file_name=filename, file_path=save_path, ticket_id=t_id, uploaded_by=uploaded_by)
        return (jsonify({'message': 'File uploaded successfully', 'attachment': attachment.to_dict()}), 201)
    return (jsonify({'message': 'File type not allowed'}), 400)

@ticket_bp.route('/api/tickets/<int:t_id>/history', methods=['GET'])
@jwt_required()
def api_view_history(t_id):
    ticket_history = history_service.get_history_by_ticket(t_id)
    if ticket_history:
        history_list = [h.to_dict() for h in ticket_history]
        return (jsonify({'message': 'Ticket History', 'ticket_history': history_list}), 200)
    return (jsonify({'message': 'No history found for this ticket'}), 404)

@ticket_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard_page():
    claims = get_jwt()
    role = claims.get('role')
    user_id = get_jwt_identity()
    username = claims.get('username')
    stats = None
    if role == 'ADMIN':
        tickets = ticket_service.get_all_ticket()
        stats = ticket_service.get_dashboard_stats()
    elif role == 'SUPPORT_AGENT':
        all_tickets = ticket_service.get_all_ticket()
        tickets = [t for t in all_tickets if str(t.assigned_to) == str(user_id) or t.assigned_to is None]
    else:
        tickets = ticket_service.get_ticket_by_user_id(user_id)
    return render_template('dashboard.html', tickets=tickets, stats=stats, role=role, username=username, user_id=user_id)

@ticket_bp.route('/tickets/new', methods=['GET', 'POST'])
@jwt_required()
def create_ticket_page():
    if request.method == 'GET':
        categories = category_service.get_all_category()
        return render_template('create_ticket.html', categories=categories)
    title = request.form.get('title')
    description = request.form.get('description')
    category_id = request.form.get('category_id')
    priority = request.form.get('priority')
    current_user_id = get_jwt_identity()
    ticket_service.add_ticket(title, description, category_id, current_user_id, priority)
    return redirect('/dashboard')

@ticket_bp.route('/tickets/<int:t_id>', methods=['GET'])
@jwt_required()
def ticket_detail_page(t_id):
    ticket = ticket_service.get_ticket_by_id(t_id)
    comments = comment_service.get_comments_by_ticket(t_id)
    attachments = ticket_attachment_service.get_ticket_attachment_by_ticket_id(t_id)
    claims = get_jwt()
    role = claims.get('role')
    agents = []
    if role == 'ADMIN':
        agents = [u for u in user_service.get_all_user() if u.roles and u.roles.roles == 'SUPPORT_AGENT']
    return render_template('ticket_detail.html', ticket=ticket, comments=comments, role=role, agents=agents, attachments=attachments)

@ticket_bp.route('/uploads/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@ticket_bp.route('/tickets/<int:t_id>/attachments_web', methods=['POST'])
@jwt_required()
def upload_file_web(t_id):
    if 'file' not in request.files:
        return redirect(f'/tickets/{t_id}')
    file = request.files['file']
    if file.filename == '':
        return redirect(f'/tickets/{t_id}')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        uploaded_by = get_jwt_identity()
        ticket_attachment_service.add_ticket_attachment(file_name=filename, file_path=save_path, ticket_id=t_id, uploaded_by=uploaded_by)
    return redirect(f'/tickets/{t_id}')

@ticket_bp.route('/tickets/<int:t_id>/assign_web', methods=['POST'])
@jwt_required()
def assign_ticket_web(t_id):
    claims = get_jwt()
    if claims.get('role') != 'ADMIN':
        return redirect(f'/tickets/{t_id}')
    agent_id = request.form.get('assigned_to')
    if agent_id:
        ticket_service.update_ticket_assignment(t_id, agent_id)
    return redirect(f'/tickets/{t_id}')

@ticket_bp.route('/tickets/<int:t_id>/comments', methods=['POST'])
@jwt_required()
def add_comment_page(t_id):
    comment_text = request.form.get('comment')
    user_id = get_jwt_identity()
    comment_service.add_comment(t_id, user_id, comment_text)
    return redirect(f'/tickets/{t_id}')

@ticket_bp.route('/tickets/<int:t_id>/update', methods=['POST'])
@jwt_required()
def update_ticket_web(t_id):
    claims = get_jwt()
    if claims.get('role') not in ['ADMIN', 'SUPPORT_AGENT']:
        return redirect(f'/tickets/{t_id}')
    status = request.form.get('status')
    priority = request.form.get('priority')
    user_id = get_jwt_identity()
    if status:
        ticket_service.update_ticket_status(t_id, status, user_id)
    if priority:
        ticket_service.update_ticket_priority(t_id, priority)
    return redirect(f'/tickets/{t_id}')