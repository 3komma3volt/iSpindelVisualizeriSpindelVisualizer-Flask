from ispindelVisualizer import db, login_manager
from flask_login import UserMixin
from flask_bcrypt import Bcrypt


@login_manager.user_loader
def load_user(spindle_id):
    return Spindles.query.get(spindle_id)


class Spindles(db.Model, UserMixin):
    __tablename__ = "spindles"
    id = db.Column(db.Integer, primary_key = True)
    spindle_id = db.Column(db.Integer)
    spindle_key = db.Column(db.String)
    spindle_alias = db.Column(db.String)

    def __init__(self, spindle_id: int, spindle_key: int, spindle_alias: str):

        bc = Bcrypt()

        self.spindle_id = spindle_id
        self.spindle_key = bc.generate_password_hash(spindle_key)
        self.spindle_alias = spindle_alias

class Spindle_data(db.Model):
    __tablename__ = "spindle_data"

    id = db.Column(db.Integer, primary_key = True)
    spindle_name = db.Column(db.Integer)
    spindle_id = db.Column(db.Integer)
    angle = db.Column(db.Integer)    
    temperature = db.Column(db.Integer)
    temp_units = db.Column(db.String)
    battery = db.Column(db.Integer)
    gravity = db.Column(db.Integer)
    update_interval = db.Column(db.Integer)
    rssi = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)

    def __init__(self, spindle_name: str, spindle_id: int, angle: int, temperature: int, temp_units: str, battery: int, gravity: int, update_interval: int, rssi: int, created_at: str):
        self.spindle_name = spindle_name
        self.spindle_id = spindle_id
        self.angle = angle  
        self.temperature = temperature
        self.temp_units = temp_units
        self.battery = battery
        self.gravity = gravity
        self.update_interval = update_interval
        self.rssi = rssi
        self.created_at = created_at
