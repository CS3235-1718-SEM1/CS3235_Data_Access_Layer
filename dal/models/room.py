from .. import db
from .room_access import room_accesses


class Room(db.Model):
    __tablename__ = 'rooms'

    # For this Proof-of-Concept, we'll assume that each room only has 1 door, therefore we don't have a
    # relation for door and there's a door_id column in each room tuple
    # Room is also identified by the door_id
    door_id = db.Column(db.String(32), primary_key=True)
    modules_allowed = db.relationship('Module', secondary=room_accesses, lazy='subquery', backref=db.backref('rooms_accessible', lazy=True))

    def __repr__(self):
        return '<Room with door id {}>'.format(self.door_id)

