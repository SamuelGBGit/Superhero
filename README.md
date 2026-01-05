# Superhero API

This is a small Flask API for tracking heroes and their powers. It implements the deliverables for the assessment: models, relationships, validations, and routes.

Features
- Models: `Hero`, `Power`, `HeroPower` with relationships
- Validations: `Power.description` length, `HeroPower.strength` allowed values
- Routes: GET `/heroes`, GET `/heroes/<id>`, GET `/powers`, GET `/powers/<id>`, PATCH `/powers/<id>`, POST `/hero_powers`

Getting started

1. Create a virtual environment and install requirements:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Seed the database:

```bash
python3 seeds.py
```

3. Run the app:

```bash
python3 app.py
```

API notes
- Use the Postman collection `challenge-2-superheroes.postman_collection.json` (add it to the repo and import into Postman) to test endpoints.

Routes
- `GET /heroes` — list heroes
- `GET /heroes/<id>` — get hero with `hero_powers` nested
- `GET /powers` — list powers
- `GET /powers/<id>` — get power
- `PATCH /powers/<id>` — update a power's `description` (validation applies)
- `POST /hero_powers` — create a hero-power association. Body: `{"strength":"Average","power_id":1,"hero_id":3}`

Notes on validations
- `Power.description` must be present and at least 20 characters.
- `HeroPower.strength` must be one of: `Strong`, `Weak`, `Average`.

If you want, I can add Dockerfile / runtime scripts for deployment.

Docker (optional)

Build and run with Docker (local):

```bash
# From repository root
docker build -t superhero-api .
docker run -p 5000:5000 --name superhero-api -d superhero-api

# Or using docker-compose
docker-compose up --build -d
```

The API will be available at `http://localhost:5000` when the container is running.

# Superhero