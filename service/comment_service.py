from config.database import db
from models.comment import Comment

class CommentService:

    def __init__(self, dao):
        self.comment_dao = dao

    def add_comment(self, t_id, user_id, comment_text):
        comment = Comment(ticket_id=t_id, user_id=user_id, comment=comment_text)
        return self.comment_dao.add_comment(comment)

    def get_all_comment(self):
        return self.comment_dao.get_all_comment()

    def get_comment_by_id(self, t_id):
        return self.comment_dao.get_comment_by_id(t_id)

    def get_comment_by_user_id(self, c_id):
        return self.comment_dao.get_comment_by_user_id(c_id)

    def get_comments_by_ticket(self, t_id):
        return self.comment_dao.get_comments_by_ticket_id(t_id)

    def get_comment_by_ticket_id(self, t_id):
        return self.comment_dao.get_comment_by_id(t_id)

    def update_comment(self, comment):
        return self.comment_dao.update_comment(comment)

    def delete_comment(self, c_id):
        comment = self.comment_dao.get_comment_by_id(c_id)
        return self.comment_dao.delete_comment(comment)