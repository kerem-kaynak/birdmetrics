from app.extensions.database import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    company_name = db.Column(db.String(120))
    metric = db.relationship('Metric', backref = 'user', lazy = True)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    metric_name = db.Column(db.String(120))
    month = db.Column(db.Date)
    value = db.Column(db.Numeric)