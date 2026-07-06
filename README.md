# DissHub — Django Discussion Forum

A full-featured discussion forum built with Django, HTML, CSS, and Bootstrap 5.
Users can sign up, post problems/discussions under categories, reply with comments,
mark discussions as resolved, mark a comment as the accepted solution, and like discussions.

## Features
- User registration, login, logout
- Create / edit / delete discussions
- Categories with discussion counts
- Comment / reply system
- Mark a discussion as Resolved / Open
- Mark a comment as the accepted Solution
- Like discussions
- Search (title & body) and filter by category/status
- User profiles with bio & avatar
- Pagination
- Django admin for managing all content
- Responsive Bootstrap 5 UI (navbar, cards, badges)

## Project Structure
```
forum_project/
├── forum_project/       # Project settings, urls, wsgi/asgi
├── forum/                # Main app: models, views, forms, urls, admin
├── templates/forum/       # HTML templates (Bootstrap based)
├── static/css/style.css  # Custom styling
├── seed.py               # Script to seed demo categories/users/discussion
├── manage.py
└── requirements.txt
```

## Setup Instructions

1. Extract the zip and enter the project folder:
   ```bash
   cd forum_project
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. (Optional) Seed demo data — creates sample categories, a superuser
   (`admin` / `admin12345`), a demo user (`demo` / `demo12345`), and one
   sample discussion:
   ```bash
   python manage.py shell < seed.py
   ```

6. (Optional) Create your own superuser instead:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Open your browser at:
   - Forum: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Notes
- `DEBUG = True` is set for local development in `forum_project/settings.py`.
  Turn it off and set `ALLOWED_HOSTS` before deploying to production.
- Uploaded avatars are stored under `media/` (created automatically).
- To add discussion categories, use the Django admin (`/admin/`) — a few are
  seeded automatically if you ran `seed.py`.
