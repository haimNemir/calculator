# Calculator Application

This repository contains the application layer of the calculator project.

Current stack:
- Frontend: React + TypeScript + Vite
- Backend: Flask + Gunicorn
- Database: MySQL

## Repository layout

- `frontend/` contains the browser UI
- `backend/` contains the API server
- `.github/workflows/ci.yml` builds, smoke-tests, and pushes images to Amazon ECR
- `docker-compose.yml` provides a lightweight local run for the frontend and backend

## Run locally

Start the frontend and backend:

```bash
docker compose up --build
```

Local URLs:
- Frontend: `http://localhost:8080`
- Backend: `http://localhost:5000`
- Backend health: `http://localhost:5000/health`

## Important local note

The current `docker-compose.yml` does not start a local MySQL container.

That means:
- calculator operations through `/api/calc` work
- the backend health endpoint `/health` works
- database-backed features such as `/api/history` require a running MySQL instance and matching environment variables

## CI behavior

The CI workflow:
- builds the backend and frontend Docker images
- runs smoke tests for both images
- authenticates to AWS through GitHub OIDC
- pushes images to Amazon ECR for the `dev` environment

This repository is the application source only. Kubernetes manifests and Helm values live in the `calculator_desire_state` repository, and AWS infrastructure lives in the `calculator_IaC_Terra` repository.
