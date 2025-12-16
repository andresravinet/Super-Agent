# Documentation

Use this directory to capture design intent, operational notes, and onboarding material that does not live inside workflow JSON files.

## Purpose
- Centralize long-form architecture, runbooks, and decision records that guide how workflows and tools are built.
- Provide contributors with narrative context before they touch schemas, prompts, or n8n exports.

## Required file types
- Markdown (`.md`) for guides and references. Keep diagrams as embedded Markdown links or export them as `.png`/`.svg` assets checked into `docs/`.

## Naming and versioning
- Use kebab-case filenames that describe the topic, e.g., `architecture-overview.md`.
- When revising major procedures, append a semantic or date suffix (for example, `runbook-v2.md` or `prompt-style-2024-09.md`) and link the superseded file at the top.
- Cross-reference related files to keep navigation simple (e.g., link from `RUNBOOK.md` to specific `workflows/*.json` that the procedure depends on).

## Producing and consuming artifacts
- Update `ARCHITECTURE.md` when workflow graphs or routing policies change to keep code and docs aligned.
- Extend `RUNBOOK.md` with operational steps any time a new script is added under `scripts/` or when import/export flows change.
- Each guide should call out which workflow or schema it governs; for example, a playbook for approvals should cite `workflows/approval_gate.json`.
- Prefer examples pulled directly from fixtures under `tests/fixtures/` so they stay test-backed (e.g., mirror the request shape in `tests/fixtures/request_envelope.json`).

## Examples
- Architecture: see `ARCHITECTURE.md` for how `main_orchestrator.json` coordinates routing and approvals.
- Operations: `RUNBOOK.md` documents how to restart imports using `scripts/import_workflows.sh` and how to verify via `python -m unittest tests/test_workflows.py`.
