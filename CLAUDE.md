# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**NUSHire** — a fullstack web app for NUS students to discover internships, analyze skill gaps against job requirements, and log application outcomes. Built for NUS Orbital 2026 by Team JavaBuns (Apollo 11 / Milestone 2).

## Commands

### Frontend (`cd frontend` first)

```bash
npm install          # install dependencies
npm run dev          # dev server at http://localhost:5173 (proxies /api to port 8000)
npm run build        # production build
npm run lint         # ESLint
```

### Backend (project root, venv activated)

```bash
pip install -r requirements.txt
python manage.py migrate
python seed.py                        # populate skills, demo users, jobs, outcomes
python manage.py runserver            # API at http://127.0.0.1:8000
python manage.py makemigrations api   # after model changes
python manage.py test api             # run backend tests
```

### Demo credentials

- **alice / password123** — SOC CS Year 3, 3.5–4.0 GPA, strong skill profile (11 skills)
- **bob / password123** — SOC CS Year 2, 3.0–3.5 GPA, weaker profile (7 skills)

## Architecture

### Stack

- **Frontend**: React 19 + React Router 7 + Vite 8 + Tailwind CSS 4
- **Backend**: Django 6 + Django REST Framework + Token auth
- **DB**: SQLite (dev); intended for Supabase/PostgreSQL in production
- **CORS**: `CORS_ALLOW_ALL_ORIGINS=True` — dev-only, must lock down for prod

### Request Flow

```
Browser (localhost:5173)
  → Vite /api proxy
  → Django (localhost:8000)
    → Token auth middleware
    → DRF view
    → SQLite
```

Token is stored in `localStorage`, sent as `Authorization: Token <token>`. The frontend checks the token on load via `GET /api/profile/`; unauthenticated users can still browse jobs.

### API Contract

`frontend/src/api.js` is the source of truth for all endpoints. **Trailing slashes are required** — Django's `APPEND_SLASH` will 301 otherwise. Key endpoints:

| Method | Endpoint | Auth |
|--------|----------|------|
| POST | `/api/login/` | AllowAny |
| POST | `/api/signup/` | AllowAny |
| GET/PATCH | `/api/profile/` | IsAuthenticated |
| GET | `/api/jobs/` | AllowAny |
| GET | `/api/jobs/:id/` | AllowAny |
| GET | `/api/jobs/:id/skill-gap/` | IsAuthenticated |
| GET | `/api/outcomes/` | IsAuthenticated |
| POST | `/api/outcomes/submit/` | IsAuthenticated |
| GET | `/api/skills/` | AllowAny |

Global DRF default is `IsAuthenticated`; job/skill views must explicitly set `AllowAny`.

### Key Backend Patterns

**Profile auto-creation**: Every `User` must get a linked `Profile` automatically. Wire this via a `post_save` signal in `api/apps.py::ready()`.

**`skill_ids` is write-only**: `PATCH /api/profile/` accepts `skill_ids` (list of IDs), but `GET /api/profile/` returns nested skill objects. Handle in `ProfileSerializer` with a `write_only` field + `update()` override.

**Stats are computed, not stored**: `JobDetailSerializer` aggregates `ApplicationOutcome` records on every request for `total_applications`, `offer_rate`, `avg_year_of_study`, and `gpa_distribution`.

**Skill-gap engine** (`api/skill_gap.py`): Pure functions — no DB writes. Input: `Profile` + `JobListing`. Output: `match_score` (%), `strengths`, `high_priority_gaps`, `medium_priority_gaps`, `suggestions`. The target skill set is the union of the job's `required_skills` plus skills found in past successful applicants (weighted). Keep it pure so M3 can swap in weighted scoring without touching views.

### Frontend Routing

```
App.jsx (token-check on mount, sets user state)
├── / → JobListPage (public; client-side search + role_type filter)
├── /jobs/:id → JobDetailPage (public; shows skill-gap panel only when authed)
├── /jobs/:id/outcome → OutcomeSubmitPage (auth-gated)
├── /login → LoginPage
├── /signup → SignupPage
└── /profile → ProfilePage (auth-gated)
```

## Critical Note: `api/` Does Not Exist Yet

The entire Django `api/` app is missing from the repo. Nothing runs until these are created (in order):

1. `api/__init__.py`
2. `api/apps.py` — AppConfig + Profile auto-creation signal
3. `api/models.py` — Profile, SkillTag, JobListing, ApplicationOutcome, Alumni
4. `api/serializers.py`
5. `api/views.py`
6. `api/urls.py` — must match `api.js` exactly
7. `api/admin.py`
8. `api/skill_gap.py`
9. `api/migrations/__init__.py`, then `makemigrations api`

See **ROADMAP.md** for the full acceptance checklist and phase breakdown — it is the authoritative spec for Milestone 2 feature scope and build order.
