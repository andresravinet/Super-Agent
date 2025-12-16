# Workflows

n8n workflow exports orchestrating the agent stack live here.

## Purpose
- Provide import-ready JSON for the orchestrator, router, approval gate, and specialist lanes.
- Keep a single source of truth for what the automation does so tests and docs can reference concrete node graphs.

## Required file types
- n8n workflow exports (`.json`) produced via `n8n export:workflow` or the n8n UI.
- Sub-workflows under `tools/` that specialists call should also be JSON exports.

## Naming and versioning
- Name files after the workflow `name`/`id` inside the export (e.g., `main_orchestrator.json`, `router.json`, `approval_gate.json`).
- Maintain the `versionId` field to reflect the export source; when making breaking changes, increment a suffix (for example, `router-v2.json`) and keep the previous version until consumers migrate.
- Keep sub-workflow filenames scoped by tool or lane (for example, `tools/summarize_doc.json`).

## Producing and consuming artifacts
- To **export**: from your n8n instance, run `n8n export:workflow --all --output=workflows` (or export specific IDs) so the JSON lands in this directory with `tools/` containing dependencies.
- To **import**: use `scripts/import_workflows.sh`, which imports `workflows/tools/` first and then top-level orchestrator/router JSON in dependency order.
- Align workflow inputs/outputs with schemas in `schemas/` and fixtures in `tests/fixtures/`; e.g., the router’s intents must match `schemas/request_envelope.json` and `schemas/router_plan.json` as asserted in `tests/test_workflows.py`.
- When embedding prompts, reference the source files in `prompts/` to keep text parity between exports and authored templates.

## Examples
- Primary orchestrator: `main_orchestrator.json` handles intake, planning, specialist dispatch, and approval gating.
- Routing layer: `router.json` classifies requests into intents and specialists and normalizes the result before downstream tools consume it.
- Approval safety net: `approval_gate.json` encodes manual-review criteria invoked when tool calls have write/external side effects.
