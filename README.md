
---

✅  *`README.md`*

```md
Ktune 🎶

Ktune is an online event and ticket booking platform built with Django.

Features in v0.1

- Custom user model with host support
- User registration & login (email-based)
- Bootstrap-styled login/signup pages

Tech Stack

- Python 3
- Django
- Bootstrap 5
- SQLite
- decouple (for environment variables)

Setup

```bash
git clone https://github.com/br41n7/ktune.git
cd ktune
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver

