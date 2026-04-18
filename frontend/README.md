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
- `vite.config.ts` configures Vite for production builds and optional local dev-server use
- `nginx.conf` serves only the built app in the container image used by Kubernetes
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

In Kubernetes, the frontend container serves static files only. The cluster Ingress routes `/api` and health paths directly to the backend service, and routes `/` to the frontend service.

In optional local Vite development, `vite.config.ts` can proxy `/api` to `http://localhost:5000` if you choose to run the backend directly for UI iteration. No Docker Compose runtime is maintained in this repository.

The frontend expects the backend to expose:
- `POST /api/calc`
- `GET /api/history`
- `GET /health`
- `GET /health/db`

## Notes

- The frontend is project-specific documentation now; this file is no longer the default Vite template README.
- The actual built frontend output directory is `dist/`, not `build`.
