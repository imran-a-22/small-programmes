# Interview Prep Tracker (MVP)

A portfolio-ready full-stack Flask app for tracking interview question practice with spaced review.

## Features implemented
- User registration/login/logout
- Create/read/update/delete interview cards
- Tag filtering
- Confidence score (1-5)
- Auto-calculated next review date (spaced intervals)
- Daily review queue for due cards
- Dashboard stats (total, due, average confidence, cards by tag)

## Tech
- Python 3.11+
- Flask
- SQLite
- HTML templates + CSS

## Run locally
```bash
cd interview-prep-tracker
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Then open http://127.0.0.1:5000

## Step-by-step delivery approach
See [PLAN.md](./PLAN.md) for incremental phase-based execution.

## Suggested next improvements
1. Add guest mode
2. Add tests for CRUD and review scheduling
3. Add deployment config
4. Add charts on dashboard
