"""
This script populate the DB with all the modules in NUS (based on NUSMods API)
"""

import json

from .. import db
from .module import Module

with open('./dal/models/module_list.json') as f:
    modules_dict = json.load(f)

for code in modules_dict.keys():
    new_module = Module(code=code)
    db.session.add(new_module)

db.session.commit()
