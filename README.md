# TaskLens — Backend

A Django REST Framework API providing task management and image annotation endpoints with JWT authentication.

**Live API:** https://web-production-37cf.up.railway.app  
**Frontend repo:** https://github.com/Rayhan-002/tasklens-frontend  
**Demo credentials:** `rayhandummy@gmail.com` / `12345678$`

---

## ⚔️ Villains Faced & How I Defeated Them

### Villain 1 — The Serializer Context Phantom (blank images)
DRF's `ImageField` serializer builds absolute media URLs only when the HTTP request is passed in via `context={'request': request}`. Without it, the field emits bare relative paths like `/media/annotation_images/foo.jpg`. The frontend resolved these against its own origin (`localhost:3000`) — a 404 — so every canvas was blank. Defeated by passing request context to every `AnnotationImageSerializer` instantiation in the views.

### Villain 2 — The ALLOWED_HOSTS Gatekeeper
After deploying to Railway, every API call returned a raw HTML `Bad Request (400)` page — Django's security middleware was rejecting requests before they reached any view, because the `Host` header sent by Railway's proxy didn't exactly match the value in `ALLOWED_HOSTS`. Slain by setting `ALLOWED_HOSTS=*` in Railway's environment variables for the demo deployment.

### Villain 3 — The SQLite Amnesiac
Railway's filesystem is ephemeral — every redeploy wipes the SQLite database and the demo user disappears. Managed by re-creating the user via the Railway Console shell after each redeploy, and by running `python manage.py migrate` automatically on startup via the `Procfile`.

### Villain 4 — The mise Attestation Blocker
Railway's nixpacks builder uses `mise` to install Python and failed to verify GitHub artifact attestations for Python 3.12.0, aborting the build before any application code ran. Defeated by adding the environment variable `MISE_PYTHON_GITHUB_ATTESTATIONS=false` in Railway's Variables tab (Railway even provides a one-click button for this in the build error diagnosis panel).

### Villain 5 — The Production Static Files Void
Django's `static()` URL helper only activates when `DEBUG=True`. In production, uploaded media files returned 404s because the URL pattern disappeared. Fixed by replacing `static()` in `urls.py` with a direct `re_path` using `django.views.static.serve`, which works regardless of `DEBUG` mode.

---

## 🛠️ Tech Stack

- **Framework:** Django 6.0.7 + Django REST Framework 3.17
- **Auth:** `djangorestframework-simplejwt` (8h access / 7d refresh tokens)
- **CORS:** `django-cors-headers`
- **Images:** Pillow
- **Server:** Gunicorn
- **Static files:** WhiteNoise
- **Database:** SQLite (via Django ORM)

---

## ⚙️ Environment

| Tool | Version |
|------|---------|
| Python | 3.12.0 |
| Django | 6.0.7 |
| pip | bundled with Python |

---

## 🚀 Running Locally

### Prerequisites
- Python 3.12+

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/Rayhan-002/tasklens-backend
cd tasklens-backend

# 2. Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create a superuser (demo account)
python manage.py createsuperuser

# 6. Start the development server
python manage.py runserver
```

The API will be available at [http://localhost:8000](http://localhost:8000).

### Key API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/login/` | POST | Login with email + password |
| `/api/auth/me/` | GET | Current user info |
| `/api/tasks/` | GET, POST | List / create tasks |
| `/api/tasks/<id>/` | GET, PATCH, DELETE | Task detail |
| `/api/tasks/tags/` | GET, POST | Tags |
| `/api/annotations/images/` | GET, POST | Images |
| `/api/annotations/images/<id>/polygons/` | GET, POST | Polygons |

### Environment Variables (production)

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for dev, `False` for prod |
| `ALLOWED_HOSTS` | Comma-separated hostnames (use `*` for demo) |
| `CORS_ALLOWED_ORIGINS` | Comma-separated frontend origins |
| `MEDIA_ROOT` | Path to media storage directory |
