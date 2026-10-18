# Git and GitHub Assignment — Flask + MongoDB
Student: Danish | GitHub: https://github.com/Danish200170

## Routes
- `GET /` — To-Do form
- `GET /api` — returns `data.json`
- `POST /submittodoitem` — validates and inserts a To-Do document into MongoDB
- `GET /health` — MongoDB connectivity check

## Run in Ubuntu/WSL
```bash
sudo apt update
sudo apt install -y python3-venv python3-pip
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export MONGODB_URI="mongodb://localhost:27017/"
python app.py
```
Open http://127.0.0.1:5000. MongoDB must be running. The POST endpoint returns 503 when MongoDB is unavailable rather than claiming data was saved.

## Git workflow
Follow `workflow/GIT_WORKFLOW.md`. Execute the steps yourself and capture genuine terminal evidence; the guide and Word template are not proof that a workflow has been executed.
