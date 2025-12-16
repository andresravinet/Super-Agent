# Scripts

Helper scripts for development, maintenance, or deployment belong here.

## Purpose
- Automate common n8n import/export flows and repository hygiene tasks.
- Provide reproducible commands that match the steps described in `README.md` and `docs/RUNBOOK.md`.

## Required file types
- Shell scripts (`.sh`) for CLI automation; keep them POSIX-compatible where possible so they run in CI and containers.
- Supplementary Markdown files if a script needs a dedicated how-to guide.

## Naming and versioning
- Name scripts after the action they perform (e.g., `import_workflows.sh`).
- Use environment variables for configurable options instead of hardcoding paths or commands; document the variables inline with comments.
- When changing behavior in a backwards-incompatible way, introduce a suffixed copy (for example, `import_workflows_v2.sh`) and update docs/tests to reference the new entry point.

## Producing and consuming artifacts
- `import_workflows.sh` consumes workflow exports under `workflows/` (including `workflows/tools/`) and calls `n8n import:workflow` in the correct dependency order. Configure `N8N_CMD` and `N8N_IMPORT_OPTS` to point at alternate binaries or pass CLI flags.
- When exporting new workflows from n8n, drop the JSON files into `workflows/` and re-run `scripts/import_workflows.sh` to verify the import works locally.
- Keep `docs/RUNBOOK.md` aligned with any new flags or behaviors introduced here so operators know how to run the scripts.

## Examples
- Import repository defaults into the configured n8n instance:
  ```bash
  scripts/import_workflows.sh
  ```
- Import from another directory with explicit overwrite flags:
  ```bash
  N8N_IMPORT_OPTS="--separate --force" scripts/import_workflows.sh /path/to/workflows
  ```
- Target an n8n binary inside a container:
  ```bash
  N8N_CMD="docker exec my-n8n n8n" scripts/import_workflows.sh
  ```
