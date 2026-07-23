# AGENTS.md

## Cursor Cloud specific instructions

This is a single Django project (a CTF training platform, "HackLabs"). SQLite backend, no external services. Python 3.12, Django installed via the update script (`requirements.txt` pins `Django==6.0.7`).

Before running the app in a fresh VM, apply migrations (not part of the update script) and optionally seed demo data:

- `python3 manage.py migrate` — creates `db.sqlite3` (git-ignored, so it won't exist on a fresh VM).
- `python3 manage.py populate_db` — seeds `admin`/`password`, `user_1..user_5` (password `password`), categories, challenges, and a lesson. Idempotent.

Run the dev server:

- `python3 manage.py runserver --insecure 0.0.0.0:8000`
- Use `--insecure` because `DEBUG = False` in `config/settings.py`; without it the dev server won't serve static/admin CSS.

Gotchas:

- Do NOT set `DEBUG = True`: `config/urls.py` references `settings.MEDIA_URL`/`MEDIA_ROOT` (undefined) inside an `if settings.DEBUG:` block, which would crash.
- Login URL is `/users/accounts/login/` (path `accounts/login/` under the `users` app), not `/accounts/login/`.
- Standard commands: tests `python3 manage.py test`; config check `python3 manage.py check`. No linter/formatter is configured.
