from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db, login_manager
from flask_login import UserMixin
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


user_identifier = db.Table(
    'user_identifier',
    db.Column('trip_id', db.Integer, db.ForeignKey('trip.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    full_name = db.Column(db.String(51), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(60))
    country = db.Column(db.String(30))
    phone_number = db.Column(db.String(25))
    gender = db.Column(db.Enum('male', 'female'), nullable=False)
    birth_date = db.Column(db.Date)
    about_me = db.Column(db.String(120))
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    active = db.Column(db.Enum('yes', 'no'), default='yes')
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    trips = db.relationship('Trip', backref='author', lazy=True)
    trips_joined = db.relationship('Trip', secondary=user_identifier, lazy='subquery',
                                   backref=db.backref('users', lazy=True))

    def get_reset_token(self, expires_sec=1800):     # 30 minutes expiration time
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    price = db.Column(db.Integer, nullable=False)
    people_number = db.Column(db.Integer, nullable=False)
    starting_at = db.Column(db.DateTime, nullable=False)
    transport_type = db.Column(db.String(30), nullable=False)
    trip_duration = db.Column(db.Integer, nullable=False)
    details = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='trip_default.jpg')

    def __repr__(self):
        return f"User('{self.author}', '{self.location}', '{self.date_created}')"
