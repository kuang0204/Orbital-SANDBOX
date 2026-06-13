# NUSHire — Project Roadmap & Requirements Document

**Team JavaBuns · Orbital 2026 · Target: Apollo 11**
**Repo:** `kuang0204/Orbital6872---NUSHire`

This is the master planning document. It is written to be the single source of truth that all
subsequent building is based on. It is organised in two parts:

- **Part A — Milestone 2 (Prototype).** The immediate, top‑priority body of work. Detailed
  file‑by‑file so each item can be picked up and built directly.
- **Part B — Transition to the final product (Milestone 3 / Apollo 11 completion).** The path
  from a working prototype to the full feature set described in the proposal.

Everything below is grounded in the *actual current state* of the repo, not the idealised plan.

---

## 0. Current State Assessment (as of this document)

### 0.1 What already exists

**Backend (Django project scaffold only)** — `backend/`
- `backend/settings.py` — DRF + `rest_framework.authtoken` + `corsheaders` configured;
  `INSTALLED_APPS` references an app called `api`; DB is **SQLite** (not Supabase/PostgreSQL
  yet, despite the proposal); token auth + session auth; `IsAuthenticated` default permission.
- `backend/urls.py` — routes `admin/` and `api/` → `include('api.urls')`.
- `backend/wsgi.py`, `backend/asgi.py`, `backend/__init__.py` — standard.
- `manage.py` (root), `seed.py` (root).

**Frontend (React + Vite + Tailwind, largely built)** — `frontend/src/`
- `api.js` — fetch wrapper with token auth. Declares every endpoint the app needs:
  `/login/`, `/signup/`, `/profile/` (GET/PATCH), `/jobs/`, `/jobs/:id/`,
  `/jobs/:id/skill-gap/`, `/outcomes/`, `/outcomes/submit/`, `/skills/`.
- `App.jsx` — routing + token-based auth gating.
- `components/Navbar.jsx`
- `pages/LoginPage.jsx`, `pages/SignupPage.jsx`
- `pages/ProfilePage.jsx` — faculty/major/year/GPA dropdowns, toggleable skill tags,
  experiences/projects/portfolio/LinkedIn fields, completion bar.
- `pages/JobListPage.jsx` — search + role-type filter, applicant count + offer rate.
- `pages/JobDetailPage.jsx` — required skills, NUS applicant stats (total apps, offer rate,
  avg year, GPA distribution), skill-gap panel (match score, strengths, gaps, suggestions),
  outcome CTA.
- `pages/OutcomeSubmitPage.jsx` — status/channel/interview-format/timeline/notes form.
- `vite.config.js` — proxies `/api` → `http://127.0.0.1:8000`.

**Seed data** — `seed.py`
- Imports `SkillTag, JobListing, ApplicationOutcome, Profile` from `api.models`.
- Creates ~42 skill tags, 2 demo users (alice/bob) with profiles + skills, 8 job listings with
  required skills, 2 sample outcomes. **This file is effectively the spec for the data model.**

### 0.2 What is MISSING (the blocker)

> The entire Django `api` app does not exist in the repo. Nothing in the backend actually runs.

Missing files (all must be created — see Part A, Phase 0):
- `api/__init__.py`
- `api/apps.py`
- `api/models.py`  ← `Profile`, `SkillTag`, `JobListing`, `ApplicationOutcome` (+ `Alumni`)
- `api/serializers.py`
- `api/views.py`
- `api/urls.py`
- `api/admin.py`
- `api/skill_gap.py` (skill-gap engine, kept separate from views)
- `api/migrations/__init__.py` (+ generated migrations)
- `api/tests/` (test suite — required for the M2 evaluation)

Also missing / incomplete:
- **Alumni feature entirely absent.** Proposal core feature #3 and M2 requirement
  "integration of alumni LinkedIn profiles" — no model, no API, no UI rendering.
- **`requirements.txt`** — no Python dependency manifest committed.
- **`README.md`** — currently one line. The M2 evaluation grades the README heavily.
- **No tests, no deployment, no project log, no poster/video.**
- **DB mismatch** — proposal promises Supabase/PostgreSQL; repo uses SQLite.

### 0.3 Gap between repo and Milestone 2 requirements

| M2 requirement (from proposal §Timeline·2) | Current repo status |
|---|---|
| (a) Job listing: dynamic data, filter/search, **alumni LinkedIn integration** | Frontend filter/search done; **no backend**; **no alumni** |
| (b) User profile: better data models, **persistent storage** | Frontend done; **no models/DB** |
| (c) Skill gap: clear missing-skill ID + simple match scoring | Frontend panel done; **no engine** |
| (d) Feedback/recommendation: suggest skills/projects/modules | Frontend renders suggestions; **no logic** |
| (e) Outcome submission: stored + linked to jobs & profiles | Frontend form done; **no persistence** |

**Conclusion:** the frontend is ahead of the backend by an entire app. Milestone 2 is
overwhelmingly a *backend + integration + documentation + deployment* effort, not new UI.

---

# PART A — MILESTONE 2 (PROTOTYPE)

Goal: a **deployed, peer-testable** prototype where all five core features work end-to-end,
with evidence of software-engineering practice (tests, version control, modular design) and
complete documentation (README, poster, video, log). This directly targets every section of
`Milestone_2_Evaluation_Form.pdf`.

The work is sequenced so that nothing is blocked by something built later.

---

## Phase 0 — Build the missing backend `api` app (CRITICAL, do first)

Without this, nothing runs. Build at the **repo root** as `api/` (sibling to `backend/` and
`frontend/`), because `backend/urls.py` does `include('api.urls')`, `manage.py` is at root, and
`seed.py` does `from api.models import ...`.

### File: `api/__init__.py`
Empty package marker.

### File: `api/apps.py`
Standard `AppConfig` (`name = 'api'`). Use the `ready()` hook to import signals (so a `Profile`
is auto-created whenever a `User` is created — see models).

### File: `api/models.py`  *(this is the heart of Phase 0 — derive fields from `seed.py`)*
Define exactly the models `seed.py` already assumes, plus `Alumni`:

- **`SkillTag`**
  - `name` (CharField, unique)
  - `category` (CharField — e.g. Language, Database, Frontend, Backend, AI/ML, Soft Skill…)
  - `__str__` → name

- **`Profile`** (OneToOne with `auth.User`)
  - `user` (OneToOneField → User, `related_name='profile'`, `on_delete=CASCADE`)
  - `faculty` (CharField with choices: SOC/ENG/BIZ/FASS/SCI/MED/LAW)
  - `major` (CharField, blank)
  - `year_of_study` (CharField choices '1'–'6', blank)
  - `gpa_range` (CharField choices: '0.0-2.0','2.0-3.0','3.0-3.5','3.5-4.0','4.0-5.0', blank)
  - `experiences` (TextField, blank)
  - `projects` (TextField, blank)
  - `portfolio_links` (TextField, blank)
  - `linkedin_url` (URLField, blank)  ← **referenced by `ProfilePage.jsx`, not in seed; add it**
  - `skills` (ManyToManyField → SkillTag, blank)
  - Use a `post_save` signal on `User` to auto-create the linked `Profile`.

- **`JobListing`**
  - `company` (CharField)
  - `role` (CharField)
  - `description` (TextField)
  - `application_link` (URLField)
  - `deadline` (DateField, null/blank)
  - `role_type` (CharField choices — must include all the frontend uses:
    SWE, DS, PM, UIUX, DE, ML, FS, IT, BA, OT)
  - `required_skills` (ManyToManyField → SkillTag, blank)
  - `__str__` → "company — role"
  - **Note:** stats (`total_applications`, `offer_rate`, `avg_year_of_study`,
    `gpa_distribution`) are **computed in the serializer**, NOT stored — they derive from
    `ApplicationOutcome` rows. Keep them out of the model.

- **`ApplicationOutcome`**
  - `user` (FK → User, `related_name='outcomes'`)
  - `job` (FK → JobListing, `related_name='outcomes'`)
  - `status` (CharField choices: offer/rejection/pending)
  - `channel` (CharField choices: portal/linkedin/careerfair/referral/email/other, blank)
  - `interview_format` (CharField choices: online/inperson/both/none, blank)
  - `timeline` (CharField, blank)
  - `notes` (TextField, blank — the "what I wish I had prepared" field)
  - `created_at` (DateTimeField, auto_now_add)
  - `Meta`: optionally `unique_together = ('user','job')` so one outcome per user per job.

- **`Alumni`**  *(new — required for M2 alumni integration; currently absent everywhere)*
  - `name` (CharField)
  - `linkedin_url` (URLField)
  - `email` (EmailField, blank)
  - `company` (CharField — matched to `JobListing.company` to surface on listing pages)
  - `current_role` (CharField, blank)
  - `graduation_year` (IntegerField, null/blank)
  - `faculty` (CharField choices, blank)
  - Rationale: proposal says alumni "lose access to their NUS email," register with email +
    LinkedIn, and are surfaced per-company on individual listing pages with current role,
    graduation year, faculty. Matching on `company` (string) is sufficient for M2; a proper FK
    to a `Company` table is an M3 refinement.

### File: `api/serializers.py`
- `SkillTagSerializer` — id, name, category.
- `UserSerializer` — id, username, email (read-only nested where needed).
- `ProfileSerializer`
  - Nested read of `user` (username/email) and `skills` (full SkillTag objects).
  - Writable `skill_ids` (PrimaryKeyRelated, write-only, maps to `skills`) — `ProfilePage.jsx`
    sends `skill_ids`.
  - All profile fields above.
- `AlumniSerializer` — name, linkedin_url, current_role, graduation_year, faculty (hide email).
- `JobListSerializer` (list view — lightweight)
  - id, company, role, role_type, deadline, plus **computed** `total_applications`,
    `offer_rate`. Use `SerializerMethodField`s that aggregate `job.outcomes`.
- `JobDetailSerializer` (detail view — rich; extends list)
  - adds `description`, `application_link`, `required_skills` (nested),
    `avg_year_of_study`, `gpa_distribution` (dict of gpa_range → count among offers),
    and `alumni` (filter `Alumni.objects.filter(company=job.company)`).
  - **Stats definitions (single source of truth):**
    - `total_applications` = count of outcomes for the job.
    - `offer_rate` = round(offers / total_applications * 100), 0 if none.
    - `avg_year_of_study` = mean `year_of_study` of users with an **offer** outcome.
    - `gpa_distribution` = `{gpa_range: count}` of **offer** applicants' profiles.
- `OutcomeSerializer` — full fields; `user` read-only (taken from request).
- `SkillGapSerializer` (or just return a plain dict from the engine) — match_score,
  strengths, high_priority_gaps, medium_priority_gaps, suggestions.

### File: `api/skill_gap.py`  *(keep the engine isolated — clean SE practice + testable)*
Pure functions, no DB writes. Input: a user `Profile` + a `JobListing`. Output: dict.
- **M2 logic (target = "usable level, simple match scoring"):**
  1. Build the **target skill set** = union of `job.required_skills` *and* the skills held by
     past **successful** applicants (offer outcomes) for that job (the "composite profile").
     Weight a skill higher if many successful applicants had it.
  2. `match_score` = round(|user_skills ∩ target| / |target| * 100).
  3. `strengths` = user skills that are in the target set.
  4. `high_priority_gaps` = target skills the user lacks that are also in `required_skills`
     (or held by a high fraction of successful applicants).
  5. `medium_priority_gaps` = remaining target skills the user lacks.
  6. `suggestions` = human-readable strings, e.g. "Add **PostgreSQL** — 80% of successful NUS
     applicants for this role had it" / "Consider a project using React to strengthen your fit."
- Keep the function signature stable; M3 will swap in weighted scoring without touching views.

### File: `api/views.py`
Use DRF. Group by feature. Auth-exempt where noted (`AllowAny`).
- `signup` (POST, AllowAny) — create User, return `{token, user}` (matches `App.handleAuth`).
- `login` (POST, AllowAny) — validate creds, return `{token, user}`.
- `ProfileView` (GET/PATCH, IsAuthenticated) — get/update `request.user.profile`;
  accept `skill_ids`.
- `JobListView` (GET, AllowAny) — list jobs; support `?role_type=` and `?search=` filtering
  (frontend currently filters client-side, but backend filtering is the M2 "dynamic data
  handling" requirement — implement it server-side too).
- `JobDetailView` (GET, AllowAny) — one job with rich stats + alumni.
- `skill_gap` (GET, IsAuthenticated) — run `skill_gap.py` for `request.user` + job id.
- `OutcomeListView` (GET, IsAuthenticated) — the current user's outcomes.
- `submit_outcome` (POST, IsAuthenticated) — create/update an outcome for `request.user`.
- `SkillListView` (GET, AllowAny) — all SkillTags (drives the profile skill picker).

> **Permission note:** job *browsing* must work logged-out (the frontend lets anonymous users
> view `JobListPage`/`JobDetailPage`), so those endpoints need `AllowAny`, overriding the
> global `IsAuthenticated` default in `settings.py`.

### File: `api/urls.py`
Wire every path to match `frontend/src/api.js` **exactly** (trailing slashes included):
`signup/`, `login/`, `profile/`, `jobs/`, `jobs/<int:pk>/`, `jobs/<int:pk>/skill-gap/`,
`outcomes/`, `outcomes/submit/`, `skills/`.

### File: `api/admin.py`
Register all five models so data can be inspected/curated via Django admin (also lets the team
manually curate the "manually curated" job board the proposal describes).

### File: `api/migrations/__init__.py`
Then run `makemigrations api` to generate the initial migration.

### Root file: `requirements.txt` *(new)*
Pin: `Django`, `djangorestframework`, `django-cors-headers`, and (when moving to Postgres)
`psycopg2-binary`, `dj-database-url`. Commit this — the evaluators/teammates need a reproducible
setup.

### Phase 0 exit criteria
- `python manage.py makemigrations && migrate` runs clean.
- `python seed.py` populates the DB without import errors.
- `python manage.py runserver` + `npm run dev` → log in as `alice`, browse jobs, view a detail
  page with stats, see a skill-gap analysis, submit an outcome, and see stats update.

---

## Phase 1 — Bring the five core features to "M2 standard"

With the API live, harden each core feature to the level the rubric expects.

1. **Job listings (a).** Move filter/search to the server (`?role_type=`, `?search=`) and keep
   the client filter as UX sugar. Ensure list stats (applicants, offer rate) populate from real
   outcomes. Empty-state and loading states already exist in the UI — verify they trigger.
2. **Profiles (b).** Confirm persistence round-trips (save → reload → values intact). Add basic
   server-side validation (valid faculty/year/GPA choices, well-formed LinkedIn URL) and return
   readable error messages — the rubric explicitly grades **error messages & prevention**
   (Eval §3.4).
3. **Skill gap (c).** Verify the engine returns sensible output for both a strong profile
   (alice) and a weak one (bob), and that `match_score` moves as skills are toggled.
4. **Feedback/recommendation (d).** Ensure `suggestions` are specific and actionable (reference
   real skills and the % of successful applicants), not generic.
5. **Outcomes (e).** Confirm a submitted outcome is linked to both user and job, feeds the
   composite profile, and immediately changes the job's stats and a user's skill-gap result.

---

## Phase 2 — Alumni integration (the genuinely new feature for M2)

This is the one core item with **no existing code anywhere**. It satisfies user story #3 and the
explicit M2 phrase "integration of alumni LinkedIn profiles."

- **Backend:** `Alumni` model (Phase 0), `AlumniSerializer`, and inclusion of matching alumni in
  `JobDetailSerializer` (filter by `company`). Seed a handful of alumni records (extend
  `seed.py`) so listing pages aren't empty.
- **Frontend:** add an **"NUS Alumni at this company"** section to `JobDetailPage.jsx` — a list
  of cards showing name, current role, graduation year, faculty, and an outbound LinkedIn
  button. (Small, self-contained change; the page already has a clean card layout to mirror.)
- **Optional alumni onboarding:** a minimal public form/endpoint to register an alumnus
  (name + email + LinkedIn + company). Can be deferred to M3 if time is tight, but the *display*
  side must ship in M2.

### Update: `seed.py`
Add alumni records keyed to existing seeded companies (Google, Meta, Shopee, …) so the alumni
section renders during the demo/video.

---

## Phase 3 — Testing (required evidence for the evaluation)

Eval §3.6 asks which correctness methods you used (Unit / Integration / System / Regression /
Automated UI). Eval §3.7 grades your **test cases**. You must have real, non-trivial tests.

### Directory: `api/tests/`
- `tests/__init__.py`
- `tests/test_models.py` — Profile auto-creation on signup; M2M skills; outcome↔job linkage;
  `unique_together` enforcement.
- `tests/test_skill_gap.py` — **the highest-value tests** (pure logic, no HTTP). Cover:
  perfect match (100), zero skills (0), partial match math, correct high vs medium gap
  classification, composite-profile influence from a seeded offer.
- `tests/test_api.py` — integration tests via DRF `APIClient`: signup→token→authed profile
  PATCH; logged-out job browsing allowed; logged-in skill-gap; outcome submission updates job
  stats.
- Target a meaningful, representative suite (not exhaustive — the rubric explicitly says a
  convincing summary with good representative examples suffices).

### Frontend (light, optional but valuable)
- A couple of component tests (Vitest + React Testing Library) for `JobListPage` filtering and
  the auth flow, *or* document a **manual test matrix** instead. Either earns the points if
  recorded in the README.

### Usability evaluation (Eval §3.5)
Run at least one lightweight method and **write it up** (even a small one counts):
expert/self walkthrough or a 3–5 person usability test with NUS friends. Record findings +
the changes you made in response. This is cheap and directly scored.

---

## Phase 4 — Deployment, documentation & deliverables

Eval §4 weights this heavily: README, poster, video, project log, and a **prototype that peers
can actually test** ("available for testing... works well in general" is the top band in §4.4).

### 4.1 Deployment (so the prototype is testable by evaluators)
- **Backend:** deploy Django (e.g. Render / Railway / Fly) with the Postgres/Supabase DB.
- **Frontend:** deploy the Vite build (e.g. Vercel / Netlify); point its API base at the live
  backend instead of the localhost proxy.
- **DB migration to Supabase/PostgreSQL** (aligns repo with the proposed stack): swap the
  `DATABASES` block in `settings.py` to read from `DATABASE_URL` via `dj-database-url`, add the
  Supabase connection string, re-run migrations + seed. Do this now so the deployed prototype
  matches the proposal's tech stack and is genuinely persistent.
- Provide demo credentials (alice/password123) in the README and on the poster.

### 4.2 `README.md` (rewrite — currently one line)
Must contain (mapped to Eval §4.1, §4.3, §4.5):
- Project purpose & motivation (condensed from the proposal).
- Live demo URL + demo login.
- The five core features, each with a one-line description and a screenshot/GIF.
- **Clear spec of the M3 (next-phase) features** — Eval §2 grades how well the *next* phase is
  specified (user role, goal, benefit, design, complexity for each).
- Tech stack + an architecture note: React/Vite ↔ DRF ↔ Postgres; how skill-gap is computed.
- Local setup instructions (backend venv + `requirements.txt` + migrate + seed; frontend
  `npm i` + `npm run dev`).
- **Software-engineering practices** evidence: modular `api` app, feature-branch Git workflow,
  isolated `skill_gap.py`, test suite, incremental development — Eval §4.5 looks for this
  explicitly.
- A short **testing section**: methods used + representative test cases (covers §3.6/§3.7).

### 4.3 Project log
- A `PROJECT_LOG.md` (or the official Orbital log) recording **time spent per member per task**.
  Eval §4.7 specifically grades whether evaluators can see how much time was invested and on
  what. Start backfilling this now and keep it current.

### 4.4 Poster & video
- **Poster:** purpose, scope, the five features, architecture diagram, screenshots.
- **Video:** a walkthrough demo of the live prototype (login → browse/filter → job detail with
  stats + alumni → skill gap → submit outcome → stats update). Keep it tight and feature-led;
  Eval §4.2 penalises videos that just repeat the README.

---

## Milestone 2 Acceptance Checklist (map directly to the evaluation form)

Tick each before submitting:

- [ ] **§1 Acceptance:** all 5 core features demonstrably work on the live URL.
- [ ] **§2 Next-phase spec:** M3 features specified in README with role/goal/benefit/design/
      complexity.
- [ ] **§3.1–3.3 Usability:** novice/expert/memorability addressed; UI is consistent (it
      already is — keep it).
- [ ] **§3.4 Utility & errors:** real error messages + input validation present.
- [ ] **§3.5 Suitability methods:** at least one usability evaluation written up.
- [ ] **§3.6 Correctness methods:** unit + integration tests committed.
- [ ] **§3.7 Test cases:** representative, non-trivial, systematically designed.
- [ ] **§4.1–4.3 Docs:** README + poster + video complete and consistent.
- [ ] **§4.4 Prototype:** deployed, reachable, testable with demo creds.
- [ ] **§4.5 SE practices:** evidenced in README + visible in repo (branches, modular app, tests).
- [ ] **§4.7 Log:** time-per-member documented.
- [ ] **§6 Self-assessment:** prototype is solid enough to read as 3–4★ (Apollo 11 band).

---

# PART B — TRANSITION TO THE FINAL PRODUCT (Milestone 3 / Apollo 11)

Once the M2 prototype is deployed and stable, M3 is *refinement + extensions*, per the proposal
§Timeline·3. The architecture from Part A is designed so these slot in without rewrites.

## B.1 Refine the skill-gap analyser (proposal 3a)
- In `api/skill_gap.py`, replace simple set-overlap with **weighted scoring**: weight each
  target skill by the fraction of successful applicants who held it; weight `required_skills`
  higher; produce true **priority-based** gaps (high/medium already structured for this).
- No view/serializer/frontend change needed — the engine's output contract stays the same.

## B.2 Success benchmarking from outcome data (proposal 3b)
- New serializer fields / endpoint comparing a user's profile against the composite successful
  profile (e.g. "you match 7/10 traits of successful applicants; you're ahead on X, behind on
  Y"). Add a benchmarking panel to `JobDetailPage.jsx`.

## B.3 Extension features (proposal 6–8)
- **Job recommendations** (`extension`): new endpoint ranking jobs by field-of-study + skill-tag
  overlap; new `RecommendationsPage.jsx`. Reuses `JobListSerializer`.
- **Sample successful portfolios** (`extension`): a `PortfolioArchetype` model curated per area
  of study; a page rendering archetypes. Curate via Django admin.
- **Bookmark / save jobs** (`extension`): `SavedJob` (user↔job) model + `save/unsave` endpoints
  + a "Saved" page; add a save button to job cards/detail.

## B.4 Alumni onboarding (if deferred from M2)
- Public alumni self-registration (email + LinkedIn + company), light moderation via admin.

## B.5 UI/UX polish (proposal 3d)
- Dashboard polish, navigation, empty/error states, mobile responsiveness, accessibility pass.

## B.6 Final-phase engineering hygiene
- CI (GitHub Actions) running the test suite on each PR (reinforces the feature-branch workflow
  the proposal commits to).
- Expand tests to cover the new M3 endpoints (regression safety).
- Final deployment hardening: real `SECRET_KEY` from env, `DEBUG=False`, restricted
  `ALLOWED_HOSTS` and CORS origins (currently `'*'` / `CORS_ALLOW_ALL_ORIGINS=True` — fine for
  dev, must be locked down for the final product).

---

## Suggested build order (dependency-aware)

1. **Phase 0** — `api` app (models → migrations → serializers → views → urls → admin →
   skill_gap), `requirements.txt`, run `seed.py`. *(Unblocks everything.)*
2. **Phase 1** — harden the 5 core features against the API; server-side filtering + validation.
3. **Phase 2** — alumni model + serializer + detail-page section + seed alumni.
4. **Phase 3** — tests (skill_gap first, then API integration) + one usability study.
5. **Phase 4** — migrate to Supabase/Postgres, deploy backend + frontend, write README,
   project log, poster, video.
6. **Submit M2**, self-check against the acceptance checklist.
7. **Part B** — M3 refinements + extensions on top of the now-stable base.

---

### Appendix — endpoint ↔ frontend contract (must not drift)

| `api.js` call | Method | URL | View | Auth |
|---|---|---|---|---|
| `login` | POST | `/api/login/` | `login` | AllowAny |
| `signup` | POST | `/api/signup/` | `signup` | AllowAny |
| `getProfile` | GET | `/api/profile/` | `ProfileView` | Auth |
| `updateProfile` | PATCH | `/api/profile/` | `ProfileView` | Auth |
| `getJobs` | GET | `/api/jobs/?role_type=&search=` | `JobListView` | AllowAny |
| `getJob` | GET | `/api/jobs/:id/` | `JobDetailView` | AllowAny |
| `getSkillGap` | GET | `/api/jobs/:id/skill-gap/` | `skill_gap` | Auth |
| `getOutcomes` | GET | `/api/outcomes/` | `OutcomeListView` | Auth |
| `submitOutcome` | POST | `/api/outcomes/submit/` | `submit_outcome` | Auth |
| `getSkills` | GET | `/api/skills/` | `SkillListView` | AllowAny |

Keep trailing slashes and field names identical to `api.js`, `ProfilePage.jsx`
(`skill_ids`), and `JobDetailPage.jsx` (`match_score`, `strengths`, `high_priority_gaps`,
`suggestions`, `gpa_distribution`, `avg_year_of_study`). Any rename must be made in both places.
