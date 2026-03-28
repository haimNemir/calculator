# Calculator Frontend

This directory contains the frontend for the calculator application.

## Stack

- React
- TypeScript
- Vite
- Nginx for serving the built frontend image

## Main responsibility

The frontend provides a small browser UI for:
- entering two numbers
- choosing an arithmetic operation
- sending calculation requests to the backend
- showing the returned result
- loading calculation history from the backend

## Key files

- `src/App.tsx` contains the main calculator UI and fetch logic
- `src/main.tsx` mounts the React application
- `nginx.conf` serves the built app and forwards `/api/` requests to the backend service
- `nginx.ci.conf` serves only static files for frontend smoke tests in CI
- `Dockerfile` builds the frontend assets and packages them into an Nginx image

## Development

Install dependencies:

```bash
npm ci
```

Run the Vite development server:

```bash
npm run dev
```

Build the production bundle:

```bash
npm run build
```

Lint the code:

```bash
npm run lint
```

## Runtime behavior

In containerized and Kubernetes environments, Nginx serves the built frontend and proxies `/api/` requests to the backend service on port `5000`.

The frontend expects the backend to expose:
- `POST /api/calc`
- `GET /api/history`
- `GET /health`
- `GET /health/db`

## Notes

- The frontend is project-specific documentation now; this file is no longer the default Vite template README.
- The actual built frontend output directory is `dist/`, not `build/`.
