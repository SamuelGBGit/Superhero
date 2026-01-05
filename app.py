import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, setup_db, Hero, Power, HeroPower


# Read database URL from environment (Render/Heroku provide DATABASE_URL)
def get_database_uri():
    return os.environ.get('DATABASE_URL') or os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///superheroes.db'

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=get_database_uri(),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    setup_db(app)
    migrate = Migrate(app, db)

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({"status": "ok"}), 200

    @app.route('/heroes', methods=['GET'])
    def get_heroes():
        heroes = Hero.query.all()
        return jsonify([h.to_dict() for h in heroes])

    @app.route('/heroes/<int:hero_id>', methods=['GET'])
    def get_hero(hero_id):
        hero = Hero.query.get(hero_id)
        if not hero:
            return jsonify({"error": "Hero not found"}), 404
        return jsonify(hero.to_dict(include_hero_powers=True))

    @app.route('/powers', methods=['GET'])
    def get_powers():
        powers = Power.query.all()
        return jsonify([p.to_dict() for p in powers])

    @app.route('/powers/<int:power_id>', methods=['GET'])
    def get_power(power_id):
        power = Power.query.get(power_id)
        if not power:
            return jsonify({"error": "Power not found"}), 404
        return jsonify(power.to_dict())

    @app.route('/powers/<int:power_id>', methods=['PATCH'])
    def update_power(power_id):
        power = Power.query.get(power_id)
        if not power:
            return jsonify({"error": "Power not found"}), 404
        data = request.get_json() or {}
        desc = data.get('description')
        if desc is None:
            return jsonify({"errors": ["description is required"]}), 400
        try:
            power.description = desc
            db.session.add(power)
            db.session.commit()
        except ValueError as ve:
            db.session.rollback()
            errs = getattr(power, 'errors', []) or [str(ve)]
            return jsonify({"errors": errs}), 400
        except Exception:
            db.session.rollback()
            errs = getattr(power, 'errors', []) or ["invalid data"]
            return jsonify({"errors": errs}), 400
        return jsonify(power.to_dict())

    @app.route('/hero_powers', methods=['POST'])
    def create_hero_power():
        data = request.get_json() or {}
        strength = data.get('strength')
        hero_id = data.get('hero_id')
        power_id = data.get('power_id')

        if not all([strength, hero_id, power_id]):
            return jsonify({"errors": ["strength, hero_id and power_id are required"]}), 400

        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)
        if not hero or not power:
            return jsonify({"errors": ["hero or power not found"]}), 404

        try:
            hp = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
            db.session.add(hp)
            db.session.commit()
        except ValueError as ve:
            db.session.rollback()
            errs = getattr(hp, 'errors', []) or [str(ve)]
            return jsonify({"errors": errs}), 400
        except Exception:
            db.session.rollback()
            errs = getattr(hp, 'errors', []) or ["invalid data"]
            return jsonify({"errors": errs}), 400

        result = hp.to_dict(include_nested=True)
        return jsonify(result), 201

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
