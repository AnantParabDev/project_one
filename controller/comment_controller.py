from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import request, jsonify, Blueprint
from dao.comment_dao import CommentDAO
from service.comment_service import CommentService
comment_service = CommentService(CommentDAO())
comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/api/tickets/<int:t_id>/comments', methods=['GET', 'POST'])
@jwt_required()
def manage_comments(t_id):
    if request.method == 'GET':
        comments = comment_service.get_comments_by_ticket(t_id)
        comment_list = [c.to_dict() for c in comments]
        return (jsonify(comment_list), 200)
    else:
        data = request.get_json()
        comment_text = data.get('comment')
        user_id = get_jwt_identity()
        comment = comment_service.add_comment(t_id, user_id, comment_text)
        return (jsonify({'message': 'Comment added Successfully', 'comment': comment.to_dict()}), 200)