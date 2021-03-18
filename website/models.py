from . import db
from sqlalchemy.sql import func


# Creating different type of tasks and her conditions/caracteristics
class Tskrepet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_now = db.Column(db.DateTime(timezone=True), default=func.now())
    to_delete = db.Column(db.Boolean(), default=False)
    state = db.Column(db.Boolean(), default=False)
    context = db.Column(db.String(250))
    day = db.Column(db.Integer())


class TRdv(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_now = db.Column(db.DateTime(timezone=True), default=func.now())
    to_delete = db.Column(db.Boolean(), default=False)
    state = db.Column(db.Boolean(), default=False)
    context = db.Column(db.String(250))
    date = db.Column(db.DateTime())


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_now = db.Column(db.DateTime(timezone=True), default=func.now())
    to_delete = db.Column(db.Boolean(), default=False)
    state = db.Column(db.Boolean(), default=False)
    context = db.Column(db.String(250))
    date = db.Column(db.DateTime())
