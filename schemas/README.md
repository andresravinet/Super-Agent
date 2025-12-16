# Schemas

JSON Schema definitions for validating payloads and tool contracts live here.

## Purpose
- Define the shapes of request envelopes, routing plans, tool calls, and specialist outputs consumed by workflows.
- Provide a single source of truth for tests, fixtures, and any prompt examples that reference structured data.

## Required file types
- JSON Schema files (`.json`) using Draft 2020-12 (`"$schema": "https://json-schema.org/draft/2020-12/schema"`).
- Avoid YAML to keep parity with the validation harness in `tests/test_workflows.py`.

## Naming and versioning
- Name schemas after the entity they validate (e.g., `request_envelope.json`, `tool_call.json`).
- Keep schema titles and filenames aligned so `$ref` usage stays predictable.
- When breaking changes occur, clone the prior file with a version suffix such as `router_plan.v2.json` and update fixtures/tests to target the new file.

## Producing and consuming artifacts
- Author or edit schemas here, then update fixtures under `tests/fixtures/` to match.
- The test harness (`tests/test_workflows.py`) automatically validates fixtures against these schemas via `jsonschema`—run it after any schema edits.
- Workflows should only emit or accept payloads that conform to these definitions; for example, `workflows/router.json` expects an intent enumeration that mirrors `request_envelope.json` and `router_plan.json`.
- Embed `$id` values if you need to reference schemas from external tools or prompt examples.

## Examples
- `request_envelope.json` defines the inbound payload shape including intent enumeration and metadata fields.
- `tool_call.json` describes expected side effects and is enforced in fixtures like `tests/fixtures/tool_call_write.json` and by downstream checks in `tests/test_workflows.py`.
