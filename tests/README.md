# Tests

Automated tests, fixtures, and supporting assets for validating workflows live here.

## Purpose
- Guard schema compatibility, router intent coverage, and approval policies before importing workflows into n8n.
- Provide replay fixtures that mirror real payloads and tool calls.

## Required file types
- Python test modules (`test_*.py`) built on `unittest` and `jsonschema`.
- JSON fixtures under `fixtures/` that mirror the schemas in `schemas/`.
- A `requirements.txt` file enumerating test dependencies.

## Naming and versioning
- Name fixtures after the schema they satisfy (for example, `request_envelope.json`, `tool_call_write.json`).
- Keep test modules aligned with their target domain (e.g., `test_workflows.py` for workflow + schema integration checks).
- When adding new fixture variants, include an intent in the filename (`router_plan_high_risk.json`) and document the scenario in file comments or commit messages.

## Producing and consuming artifacts
- The main harness (`test_workflows.py`) loads schemas from `schemas/`, workflows from `workflows/`, and fixtures from `tests/fixtures/` to validate shapes and policies—run it after any workflow, schema, or prompt change that affects structure.
- Add new fixtures under `tests/fixtures/` and extend `test_workflows.py` to cover them when you introduce new intents, specialists, or approval criteria.
- Sync fixture examples with prompt guidance in `prompts/` to ensure generated payloads remain valid.

## Examples
- Validate everything locally:
  ```bash
  python -m pip install -r tests/requirements.txt
  python -m unittest tests/test_workflows.py
  ```
- Fixture organization:
  - `fixtures/request_envelope.json` mirrors `schemas/request_envelope.json`.
  - `fixtures/tool_call_write.json` exercises the approval-gate path enforced by `workflows/main_orchestrator.json`.
