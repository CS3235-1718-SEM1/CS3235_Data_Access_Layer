from .. import db
from .enrolment import enrolments


class Module(db.Model):
    __tablename__ = 'modules'

    code = db.Column(db.String(16), primary_key=True)

    def __repr__(self):
        return '<User {}>'.format(self.code)

