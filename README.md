# Superhero API
A Flask-based API for tracking superheroes and their powers.

## Features
- RESTful endpoints for heroes, powers, and associations
- Data validations on power descriptions and hero-power strengths
- SQLite with SQLAlchemy ORM for data management
- JSON responses with proper HTTP status codes
- Postman collection for easy testing
- Docker support for containerized deployment

## Setup Instructions

### 1. Clone and Set Up Environment
```bash
git clone <your-repo-url>
cd Superhero
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Seed the Database
```bash
python3 seeds.py
```

### 3. Run the App
```bash
python3 app.py
```
The API will be available at `http://127.0.0.1:5000`.

### 4. Test with Postman
- Import `challenge-2-superheroes.postman_collection.json`.
- Update the base URL to `http://127.0.0.1:5000`.
- Run the requests to test endpoints.

## API Endpoints
- `GET /heroes` - List all heroes
- `GET /heroes/<id>` - Get hero with powers
- `GET /powers` - List all powers
- `GET /powers/<id>` - Get specific power
- `PATCH /powers/<id>` - Update power description
- `POST /hero_powers` - Create hero-power link

## Validations
- Power descriptions must be at least 20 characters.
- Hero-power strengths: 'Strong', 'Weak', or 'Average'.

## Deployment
Render