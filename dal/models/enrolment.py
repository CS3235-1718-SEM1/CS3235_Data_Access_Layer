from .. import db

enrolments = db.Table(
    'enrolments',
    db.Column('user_ivle_id', db.String(9), db.ForeignKey('users.ivle_id'), primary_key=True),
    db.Column('module_code', db.String(16), db.ForeignKey('modules.code'), primary_key=True)
)
