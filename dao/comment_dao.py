from config.database import db
from models.comment import Comment

class CommentDAO:

    def add_comment(self, comment):
        db.session.add(comment)
        db.session.commit()
        return comment

    def get_all_comment(self):
        return Comment.query.all()

    def get_comment_by_id(self, t_id):
        return Comment.query.get(t_id)

    def get_comment_by_user_id(self, u_id):
        return Comment.query.filter_by(user_id=u_id).all()

    def get_comments_by_ticket_id(self, t_id):
        return Comment.query.filter_by(ticket_id=t_id).all()

    def update_comment(self, comment):
        db.session.commit()
        return comment

    def delete_comment(self, comment):
        db.session.delete(comment)
        db.session.commit()
        return True