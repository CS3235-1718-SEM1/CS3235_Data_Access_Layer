from .. import db
from .enrolment import enrolments


class User(db.Model):
    __tablename__ = 'users'

    ivle_id = db.Column(db.String(9), primary_key=True)
    secret_key = db.Column(db.String(64), nullable=False)
    enrolments = db.relationship('Module', secondary=enrolments, lazy='subquery', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<User {}>'.format(self.ivle_id)

