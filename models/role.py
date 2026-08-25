from config.database import db

class Role(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True)
    roles = db.Column(db.String(25), nullable=False)
    users = db.relationship('User', back_populates='roles')

    def to_dict(self):
        return {'role_id': self.role_id, 'roles': self.roles}