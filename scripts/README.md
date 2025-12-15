# Scripts

Helper scripts for development, maintenance, or deployment belong here.

## Importing workflows

Use `import_workflows.sh` to bulk import all workflows in `workflows/` and `workflows/tools/` with the correct dependency order (tool sub-workflows first, orchestrators second).

Examples:

- Import the repository defaults into the configured n8n instance:
  ```bash
  scripts/import_workflows.sh
  ```
- Import workflows from a different directory while passing additional CLI options (for example, to overwrite existing entries):
  ```bash
  N8N_IMPORT_OPTS="--separate --force" scripts/import_workflows.sh /path/to/workflows
  ```
- Point to an alternate n8n binary (e.g., inside a container):
  ```bash
  N8N_CMD="docker exec my-n8n n8n" scripts/import_workflows.sh
  ```
