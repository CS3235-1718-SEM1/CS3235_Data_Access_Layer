from .. import db


class Module(db.Model):
    __tablename__ = 'modules'

    code = db.Column(db.String(16), primary_key=True)

    def __repr__(self):
        return '<Module {}>'.format(self.code)

