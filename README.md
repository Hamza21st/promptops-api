# PromptOps — API-first Prompt Library (MVP)

Small description:
API-first service to store, version, and track prompts. Lean MVP: CRUD + API keys + basic telemetry.

Tech stack (MVP):
- Backend: FastAPI (Python) on Cloud Run
- DB: Firestore
- Auth: Firebase Auth (API key tokens)
- Docs: Docusaurus on GitHub Pages
- CI/CD: Cloud Build / GitHub Actions

Repo status: MVP planning

How to contribute:
- Open issues for microtasks
- Use labels: todo, in-progress, review, done

First issues:
- 000: Project scaffold + README (this)
- 001: FastAPI skeleton (endpoints: POST /prompts, GET /prompts)
- 002: Firestore connection
