"""Seed the database with initial data matching the deliverable examples."""
from app import create_app
from models import db, Hero, Power, HeroPower

app = create_app()

with app.app_context():
    # Clear existing
    db.drop_all()
    db.create_all()

    heroes_data = [
        ("Kamala Khan", "Ms. Marvel"),
        ("Doreen Green", "Squirrel Girl"),
        ("Gwen Stacy", "Spider-Gwen"),
        ("Janet Van Dyne", "The Wasp"),
        ("Wanda Maximoff", "Scarlet Witch"),
        ("Carol Danvers", "Captain Marvel"),
        ("Jean Grey", "Dark Phoenix"),
        ("Ororo Munroe", "Storm"),
        ("Kitty Pryde", "Shadowcat"),
        ("Elektra Natchios", "Elektra")
    ]

    powers_data = [
        ("super strength", "gives the wielder super-human strengths"),
        ("flight", "gives the wielder the ability to fly through the skies at supersonic speed"),
        ("super human senses", "allows the wielder to use her senses at a super-human level"),
        ("elasticity", "can stretch the human body to extreme lengths")
    ]

    heroes = []
    for name, super_name in heroes_data:
        h = Hero(name=name, super_name=super_name)
        db.session.add(h)
        heroes.append(h)

    powers = []
    for name, desc in powers_data:
        p = Power(name=name, description=desc)
        db.session.add(p)
        powers.append(p)

    db.session.commit()

    # Create some hero_powers
    associations = [
        (1, 1, 'Strong'),
        (1, 2, 'Strong'),
        (2, 3, 'Average'),
        (3, 1, 'Weak')
    ]
    for hero_id, power_id, strength in associations:
        hp = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
        db.session.add(hp)

    db.session.commit()
    print('Seeded database with sample heroes, powers, and hero_powers')
