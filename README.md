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

Hosting / Production deployment

Here are three recommended hosting options and the high-level steps for each. Pick the one that fits you best; I can perform any of these steps if you give repository access or the necessary service credentials.

- Render (recommended for simplicity):
	1. Create a free account at https://render.com and connect your GitHub repo.
	2. Create a new Web Service, select your repo and the `main` branch.
	3. For the Environment, choose `Docker` (Render will detect `Dockerfile`) or `Python` and set the start command to `gunicorn wsgi:app -b 0.0.0.0:$PORT --workers 2`.
	4. Set environment variables (if you add any) in the Render dashboard, and deploy. Render will automatically build and deploy on push.

- Heroku (simple, supports Procfile):
	1. Create a Heroku app and connect your GitHub repository or push with the Heroku Git remote.
	2. Ensure `Procfile`, `requirements.txt`, and `runtime.txt` exist (they are included).
	3. Enable automatic deploys from GitHub or `git push heroku main` to deploy.
	4. Use `heroku logs --tail` to monitor the app and configure environment variables in the dashboard.

- DockerHub + Cloud provider (flexible):
	1. Use the included GitHub Actions workflow to build and push an image to Docker Hub. Add `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets to the repository.
	2. Deploy the pushed image to any container host (DigitalOcean App Platform, AWS ECS/Fargate, Google Cloud Run, Fly.io, etc.).

CI / secrets
- The workflow `./github/workflows/docker-publish.yml` is a template that builds and pushes `DOCKERHUB_USERNAME/superhero-api:latest`. To use it, add two repository secrets: `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` (a Docker Hub access token).

Database note
- The project uses SQLite by default (`superheroes.db`). For production you should switch to Postgres or another managed DB. If deploying to Render/Heroku, add a Postgres instance and update `SQLALCHEMY_DATABASE_URI` via an environment variable.

# Superhero