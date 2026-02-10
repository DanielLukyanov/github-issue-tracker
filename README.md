# GitHub Issue Tracker

A small full‑stack web application that uses the GitHub API and OAuth to **view and create issues** with additional structured metadata (Client, Priority, Type) derived from labels.

This project was built as a technical assignment with a focus on **clarity, modularity, security, and maintainability** rather than feature bloat.

---

## What it does

- Authenticates users via **GitHub OAuth**
- Retrieves **all issues (open + closed)** from a repository
- Displays issues in a clean table with derived fields:
  - Client (`C:` labels)
  - Priority (`P:` labels)
  - Type (`T:` labels)
- Allows users to **create new issues** via the GitHub API
- Appends newly created issues to the current list without a full reload

---

## Tech Stack

### Backend

- **Python**
- **FastAPI** – API layer
- **HTTPX** – GitHub API / OAuth requests
- **Uvicorn** – ASGI server

### Frontend

- **Vue.js**
- **TypeScript**

### Other

- **GitHub REST API** (OAuth-based authentication)
- **Docker** for local development and deployment

---

## Labels & Data Mapping

The app derives structured fields from GitHub labels using prefixes:

- **Clients** → `C:` (e.g. `C: Client ABC`)
- **Priorities** → `P:` (Low / Medium / High)
- **Types** → `T:` (Bug / Support / Enhancement)

Only one label per prefix is expected per issue.

---

## Creating an Issue

When submitting a new issue, the user provides:

- Title
- Description (body)
- Assignee Github Username
- Client (C:)
- Priority (P:)
- Type (T:)

The backend maps these selections to GitHub labels and submits the issue through the GitHub API.

---

## Design & Code Philosophy

- **Modular structure** – clear separation between API, services, and UI
- **Extensible** – easy to add new label groups or fields
- **Minimal dependencies** – avoids heavy frameworks to expose core logic
- **Security‑aware** – OAuth flow, no tokens exposed to the frontend
- **Readable over clever** – optimized for long‑term maintenance

---

## Design Patterns (Selected)

Only the most relevant patterns are listed here — the focus was practical structure, not academic completeness.

### Backend

- **Facade Pattern** – `GitHubClient` provides a simplified interface over GitHub’s API (auth, pagination, caching)
- **DTO Pattern** – Normalizes GitHub API responses into internal representations
- **Layered Architecture** – Clear separation between API routes, services, and data transformation

### Frontend

- **Composable Pattern** – Reusable logic encapsulated via Vue composables
- **Dependency Injection** – `provide` / `inject` used to avoid prop drilling
- **Observer Pattern** – Components react to state changes via events and watchers

---

## Security Considerations

- GitHub OAuth implemented using **OAuth Apps**
- Access tokens stored **server‑side only**
- No sensitive credentials exposed to the frontend

> **CSRF Note**
>
> CSRF protection is not fully implemented in this version.
>
> Given the limited scope and time constraints of the assignment, this was an intentional trade‑off. In a production environment, CSRF tokens or strict SameSite cookie strategies would be added to all state‑changing endpoints.

---

## Performance & Scalability Notes

Issues are fetched eagerly rather than lazily paginated.

This decision was made to keep the implementation simple and predictable within the assignment scope.

For long‑term scalability, cursor‑based pagination or incremental fetching would be implemented.

---

## Environment & Deployment Notes

During development, the distinction between **development** and **production** environments became blurred.

This was a conscious consequence of learning hosting, OAuth, and deployment simultaneously:

- OAuth configuration and callback URLs required production‑like settings early on
- As a result, a traditional isolated dev environment no longer exists in this version
- This does **not** expose credentials or user data — it mainly affects local testing flexibility

In a production‑grade system, environment separation (dev / staging / prod) would be re‑established using:
- Separate OAuth apps per environment
- Environment‑specific configuration and secrets
- Mocked GitHub API responses for local development

This limitation is acknowledged and well understood.

---

## Error Handling & UX

All backend errors are propagated to the frontend in a structured way and surfaced via a custom alert system:

- Centralized backend error handling
- Consistent error payloads sent to the frontend
- Custom alert popup with:
  - Auto‑dismiss timer
  - Pause‑on‑hover behaviour

The goal was to ensure that failures are **visible, understandable, and non‑disruptive** to the user.

---

## Project Structure Notes

Some files are grouped together more tightly than they would be in a larger codebase.

Given the limited scope of the assignment, this was an intentional decision to:
- Reduce indirection
- Keep related logic easy to reason about
- Avoid premature abstraction

As the project grows, these files would naturally be split into more granular folders and modules.

---

## Learning Context

This project was built while learning several parts of the stack from scratch.

- Python was completely new
- Vue + TypeScript experience was very limited going in
- Docker was used for the first time in a real project

The focus was on delivering a **clean, working system** that could realistically be extended and maintained over time, rather than chasing completeness or polish.

The app was built by:

- Using AI as a learning aid
- Reading, refactoring, and understanding every part of the code
- Applying general software engineering best practices rather than framework magic

---

This project was built as a **stretch assignment** — intentionally reaching slightly beyond my current level.

The priority was to ship a system that works end‑to‑end, is secure, understandable, and can be reasoned about under review, even if that meant accepting a few pragmatic trade‑offs along the way.



---

## Running the Project

### Prerequisites

- **Docker** (for containerized backend)
- **Node.js** v20+
- **npm**

### Environment Variables

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_OWNER=repository_owner
GITHUB_REPO=repository_name
SESSION_SECRET=your_random_secret_key
FRONTEND_URL=http://localhost:5173
GITHUB_CLIENT_ID=your_github_oauth_app_client_id
GITHUB_CLIENT_SECRET=your_github_oauth_app_client_secret
```

### Running with Docker (Backend)

```bash
docker build -t github-issue-tracker .
docker run -p 8000:8000 --env-file .env github-issue-tracker
```

- Backend API: [http://localhost:8000](http://localhost:8000)
- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Running with npm (Frontend)

```bash
cd ui
npm install
npm run dev
```

- Frontend: [http://localhost:5173](http://localhost:5173)

### Running Locally (Without Docker)

**Backend**

```bash
pip install -r requirements/base.txt
uvicorn main:app --reload --port 8000
```

**Frontend**

```bash
cd ui
npm install
npm run dev
```
