"""
This script populate the DB with all the modules in NUS (based on NUSMods API)
"""

import json

from .. import db
from .module import Module
from .room import Room


def populate_module_list():
    with open('./dal/models/module_list.json') as f:
        modules_dict = json.load(f)

    for code in modules_dict.keys():
        new_module = Module(code=code)
        db.session.add(new_module)

    db.session.commit()


def populate_rooms():
    room1 = Room(door_id='1')
    room2 = Room(door_id='2')

    cs3235 = Module.query.filter_by(code='CS3235').first()
    room1.modules_allowed.append(cs3235)
    db.session.add(room1)
    db.session.add(room2)
    db.session.commit()
