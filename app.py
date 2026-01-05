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

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            "message": "Superhero API",
            "endpoints": ["/health", "/heroes", "/heroes/<id>", "/powers", "/powers/<id>", "/hero_powers", "/docs"]
        }), 200

    @app.route('/docs', methods=['GET'])
    def docs():
        return jsonify({
            "title": "Superhero API Documentation",
            "version": "1.0",
            "description": "API for tracking heroes and their superpowers",
            "endpoints": {
                "GET /heroes": {
                    "description": "Get a list of all heroes",
                    "response": "Array of hero objects with id, name, super_name"
                },
                "GET /heroes/<id>": {
                    "description": "Get a specific hero by ID",
                    "response": "Hero object with nested hero_powers",
                    "errors": {"404": "Hero not found"}
                },
                "GET /powers": {
                    "description": "Get a list of all powers",
                    "response": "Array of power objects with id, name, description"
                },
                "GET /powers/<id>": {
                    "description": "Get a specific power by ID",
                    "response": "Power object",
                    "errors": {"404": "Power not found"}
                },
                "PATCH /powers/<id>": {
                    "description": "Update a power's description",
                    "body": {"description": "string (min 20 chars)"},
                    "response": "Updated power object",
                    "errors": {"404": "Power not found", "400": "Validation errors"}
                },
                "POST /hero_powers": {
                    "description": "Create a hero-power association",
                    "body": {"strength": "Strong|Weak|Average", "power_id": "int", "hero_id": "int"},
                    "response": "Created HeroPower with nested hero and power",
                    "errors": {"400": "Validation errors", "404": "Hero or power not found"}
                },
                "GET /health": {
                    "description": "Health check",
                    "response": {"status": "ok"}
                },
                "GET /": {
                    "description": "API overview",
                    "response": "List of endpoints"
                }
            }
        }), 200

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
