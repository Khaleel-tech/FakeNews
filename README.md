# TruthLens - Fake News Detection Website (Django)

A complete Django web app with:
- Attractive landing page
- Registration and login authentication
- Dashboard to classify user-entered news as True/False with confidence score
- Static reference labels (Google, Reddit, Wikipedia, News Archive)
- Trending news feed with pre-classified true/false labels and scores

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Main Routes

- `/` landing page
- `/register/` account creation
- `/accounts/login/` login
- `/dashboard/` authenticated fake-news analyzer
- `/admin/` admin panel

## Notes

The detector uses a lightweight keyword-and-score heuristic in `newsapp/views.py` for demonstration.
