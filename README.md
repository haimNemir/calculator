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

## Frontend Tooling

The frontend still uses Vite as its build tool and optional local dev server.

Useful commands:

```bash
cd frontend
npm ci
npm run build
```

Optional local UI iteration:

```bash
cd frontend
npm run dev
```

This repository no longer maintains a `docker-compose` runtime. End-to-end integration is validated through the `dev` Kubernetes environment and the GitOps promotion flow.

## CI behavior

The CI workflow:
- builds the backend and frontend Docker images
- runs smoke tests for both images
- authenticates to AWS through GitHub OIDC
- pushes images to Amazon ECR for the `dev` environment
- opens a promotion PR in `calculator_desire_state` after a successful push to `main` and environment approval

This repository is the application source only. Kubernetes manifests and Helm values live in the `calculator_desire_state` repository, and AWS infrastructure lives in the `calculator_IaC_Terra` repository.

## Code Change To Deployment Flow

Use this flow when you change application code and want that change to reach the cluster through the GitOps process.

1. Make your code changes on your working branch.
2. Commit and push your branch:

```bash
git add .
git commit -m "Describe the change"
git push origin <your-branch>
```

3. Open a PR in GitHub from your branch to `calculator/main`.
4. Wait for the PR workflow to finish successfully.
   On the PR event, the workflow only builds the images and runs smoke tests.
5. Keep your local `main` branch up to date:

```bash
git switch main
git pull origin main
git switch <your-branch>
```

6. In GitHub, merge the PR into `calculator/main`.
7. After the merge, GitHub triggers the workflow again on the `push` event to `main`.
8. In that `push` run, the workflow:
   - builds the backend and frontend images again
   - runs smoke tests again
   - pushes the new image tags to Amazon ECR
   - pauses on the protected `prod-promotion` environment for approval
9. In GitHub Actions, review and approve the waiting `prod-promotion` job.
10. After approval, the workflow:
    - creates a temporary GitHub App token
    - checks out the `calculator_desire_state` repository
    - updates `environments/values-dev-images.yaml`
    - creates a new branch in `calculator_desire_state`
    - opens a PR from that branch to `calculator_desire_state/main`
11. Open the new PR in `calculator_desire_state` and review it.
12. Merge the `calculator_desire_state` PR.
13. ArgoCD detects the new commit in `calculator_desire_state/main`, syncs the desired state, pulls the new image from ECR, and deploys the updated version to the cluster.

Important note:
- The new image is pushed to ECR before the GitOps PR is merged, but the cluster is not updated until the `calculator_desire_state` PR is approved and merged.
