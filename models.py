from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

def setup_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


class Hero(db.Model):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade='all, delete')

    def to_dict(self, include_hero_powers=False):
        base = {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name
        }
        if include_hero_powers:
            base['hero_powers'] = [hp.to_dict(include_power=True) for hp in self.hero_powers]
        return base


class Power(db.Model):
    __tablename__ = 'powers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    hero_powers = db.relationship('HeroPower', back_populates='power', cascade='all, delete')

    errors = []

    @validates('description')
    def validate_description(self, key, value):
        self.errors = []
        if not value or not value.strip():
            self.errors.append('description must be present')
            raise ValueError('description must be present')
        if len(value.strip()) < 20:
            self.errors.append('description must be at least 20 characters')
            raise ValueError('description must be at least 20 characters')
        return value

    def to_dict(self):
        return {
            'description': self.description,
            'id': self.id,
            'name': self.name
        }


class HeroPower(db.Model):
    __tablename__ = 'hero_powers'
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    errors = []

    @validates('strength')
    def validate_strength(self, key, value):
        self.errors = []
        allowed = ['Strong', 'Weak', 'Average']
        if value not in allowed:
            self.errors.append(f"strength must be one of {allowed}")
            raise ValueError('invalid strength')
        return value

    def to_dict(self, include_power=False, include_nested=False):
        base = {
            'id': self.id,
            'hero_id': self.hero_id,
            'power_id': self.power_id,
            'strength': self.strength
        }
        if include_power:
            base['power'] = self.power.to_dict() if self.power else None
        if include_nested:
            base['hero'] = self.hero.to_dict()
            base['power'] = self.power.to_dict() if self.power else None
        return base
