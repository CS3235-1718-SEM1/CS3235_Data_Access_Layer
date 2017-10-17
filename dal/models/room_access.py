from .. import db

room_accesses = db.Table(
    'room_accesses',
    db.Column('module_code', db.String(16), db.ForeignKey('modules.code'), primary_key=True),
    db.Column('room_door_id', db.String(32), db.ForeignKey('rooms.door_id'), primary_key=True)
)
