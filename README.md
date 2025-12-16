# Super-Agent

Super-Agent provides a set of n8n workflows for orchestrating an executive-assistant style agent with routing, specialist tools, and approval safeguards. Use the included schemas, fixtures, and tests to validate changes before importing into your n8n instance.

- [Architecture overview](docs/ARCHITECTURE.md)
- [Workflow import script](scripts/import_workflows.sh)

## Prerequisites
- **n8n**: v1.30+ with the CLI available (`n8n import:workflow`).
- **Node.js**: v18+ to match current n8n requirements.
- **Access to n8n credentials** needed by the workflows (API keys, accounts, etc.).

## Getting the code
- Clone: `git clone https://github.com/your-org/Super-Agent.git`
- Download: use the "Download ZIP" option from GitHub, then extract the archive locally.

## Repository layout
- `workflows/`: primary orchestrator (`main_orchestrator.json`), router, specialists, approval gate, and sub-workflows under `workflows/tools/`.
- `schemas/`: JSON Schema definitions for requests, routing plans, tool calls, and specialist outputs.
- `tests/`: fixtures plus the schema/replay harness in `tests/test_workflows.py`.
- `scripts/`: helper utilities, including `scripts/import_workflows.sh` for CLI imports.
- `docs/`: design references such as `docs/ARCHITECTURE.md` describing the orchestration flow.
- `prompts/`: prompt assets used by workflows or supporting tools.

## Importing workflows
### n8n UI
1. Open **Settings → Import from File** in your n8n instance.
2. Import the tool sub-workflows from `workflows/tools/` first.
3. Import the remaining workflow JSON files (router, specialists, orchestrator, approval gate).

### CLI
- Import everything with correct ordering: `scripts/import_workflows.sh`
- Point to a custom directory: `scripts/import_workflows.sh /path/to/workflows`
- Override options (e.g., overwrite existing): `N8N_IMPORT_OPTS="--separate --force" scripts/import_workflows.sh`
- Target a remote or containerized n8n binary: `N8N_CMD="docker exec my-n8n n8n" scripts/import_workflows.sh`

## Environment configuration
- Export any credentials or environment variables required by your n8n workflows (API keys, endpoints, etc.) before running them.
- Set `N8N_CMD` if your n8n binary is not on `PATH` or runs inside a container.
- Use `N8N_IMPORT_OPTS` to pass flags such as `--separate` or `--force` during imports.

## Approval and safety model
- The orchestrator defines policies for which side effects require approval and invokes the `approval_gate` workflow before executing write or external actions.
- Approval criteria are stored in `workflows/approval_gate.json` and validated in the replay harness to ensure manual review is required when expected.

## Running tests and replay harnesses
1. Install test dependencies: `python -m pip install -r tests/requirements.txt`
2. Run the schema and replay harness: `python -m unittest tests/test_workflows.py`

The harness validates fixtures against the JSON Schemas, enforces router coverage for all declared intents, and checks that write-side tool calls trigger the approval gate before execution.
