from src.TennisApplication import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(30), nullable=False)

    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(16), nullable=False)
    city = db.Column(db.String(20), nullable=False)

    # _ = db.relationship('*', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.first_name}', " \
               f"'{self.last_name}', '{self.birth_date}', '{self.phone_number}', '{self.city}')"


class Court(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    court_number = db.Column(db.Integer, nullable=False)
    surface = db.Column(db.String(20), nullable=False)
    lights = db.Column(db.Boolean, nullable=False)
    roof = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Court('{self.court_number}', '{self.surface}', '{self.lights}', '{self.roof}')"


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    court_id = db.Column(db.Integer, db.ForeignKey('court.id'))
    date_from = db.Column(db.DateTime, nullable=False)
    date_to = db.Column(db.DateTime, nullable=False)
