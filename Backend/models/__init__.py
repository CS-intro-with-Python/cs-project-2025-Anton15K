# SQLAlchemy ORM models for the database tables.

from datetime import datetime
from ..extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    cf_handle = db.Column(db.String(100))
    rating = db.Column(db.Integer, default=1200)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    attempts = db.relationship('Attempt', backref='user', lazy=True)
    rating_adjustments = db.relationship('RatingAdjustment', backref='user', lazy=True)

    def set_password(self, password: str):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'cf_handle': self.cf_handle,
            'rating': self.rating,
            'created_at': self.created_at.isoformat() + 'Z' if self.created_at else None
        }


class Problem(db.Model):
    __tablename__ = 'problems'

    id = db.Column(db.Integer, primary_key=True)
    cf_id = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    contest_id = db.Column(db.Integer)
    problem_index = db.Column(db.String(10))
    estimated_rating = db.Column(db.Integer, default=1200)
    initial_estimated_rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    attempts = db.relationship('Attempt', backref='problem', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'cf_id': self.cf_id,
            'title': self.title,
            'contest_id': self.contest_id,
            'problem_index': self.problem_index,
            'estimated_rating': self.estimated_rating,
            'initial_estimated_rating': self.initial_estimated_rating,
            'created_at': self.created_at.isoformat() + 'Z' if self.created_at else None
        }


class Attempt(db.Model):
    __tablename__ = 'attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime)
    duration_sec = db.Column(db.Integer)
    result = db.Column(db.String(50))
    performance_rating = db.Column(db.Integer)
    time_percentile = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'problem_id': self.problem_id,
            'started_at': self.started_at.isoformat() + 'Z' if self.started_at else None,
            'ended_at': self.ended_at.isoformat() + 'Z' if self.ended_at else None,
            'duration_sec': self.duration_sec,
            'result': self.result,
            'performance_rating': self.performance_rating,
            'time_percentile': self.time_percentile
        }


class RatingAdjustment(db.Model):
    __tablename__ = 'rating_adjustments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False)
    delta = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'problem_id': self.problem_id,
            'delta': self.delta,
            'note': self.note,
            'created_at': self.created_at.isoformat() + 'Z' if self.created_at else None
        }
