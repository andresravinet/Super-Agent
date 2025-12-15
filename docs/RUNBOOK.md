# Workflow Import Runbook

This runbook documents how to import n8n workflows for Super-Agent through the UI and the CLI, including environment preparation and credential setup. Always import tool sub-workflows before orchestrators to ensure dependencies resolve correctly.

## Prerequisites and environment

- An n8n instance running with access to the database where workflows will be stored.
- The `n8n` CLI available locally (often provided by the same installation as the server).
- Set environment variables to match the target instance and database configuration before running CLI commands or scripts. Common examples:
  - `DB_TYPE`, `DB_POSTGRESDB_HOST`, `DB_POSTGRESDB_PORT`, `DB_POSTGRESDB_DATABASE`, `DB_POSTGRESDB_USER`, `DB_POSTGRESDB_PASSWORD` (or equivalent variables for your database backend)
  - `N8N_HOST`, `N8N_PORT`, `N8N_PROTOCOL` to point the CLI to the correct base URL
  - `N8N_BASIC_AUTH_USER`, `N8N_BASIC_AUTH_PASSWORD` if basic auth is enabled
- Confirm you have credentials for any external systems used by the workflows (e.g., OpenAI API key). Create or update n8n credential entries so the names match what the workflow nodes expect.

## Importing via the n8n UI

1. Sign in to the n8n UI for your environment.
2. Create credentials referenced by the workflows (e.g., OpenAI). Ensure the credential names match the nodes inside each workflow if they are already wired to credentials.
3. Import tool sub-workflows first:
   - Navigate to **Workflows** → **Import**.
   - Upload each JSON file in `workflows/tools/` (e.g., `tool_collect_research.json`, `tool_create_task.json`).
4. Import orchestrator workflows next:
   - Upload the remaining JSON files in `workflows/` (e.g., `router.json`, `main_orchestrator.json`, specialist orchestrators).
5. After import, open each workflow to verify credential assignments and activate them in the desired order (tools before orchestrators).

## Importing via the CLI

1. Export the same environment variables used by the n8n server so the CLI writes to the correct database and respects authentication.
2. From the repository root, import workflows in order:
   - First import tool workflows: `n8n import:workflow --input workflows/tools/tool_collect_research.json`
   - Then import orchestrators: `n8n import:workflow --input workflows/router.json` (repeat for the rest)
3. Alternatively, use the bulk import script:
   - Run `scripts/import_workflows.sh` (or pass a different workflows directory path as the first argument).
   - The script imports `workflows/tools/*.json` before `workflows/*.json` to preserve dependencies.
4. After the imports finish, log into the UI to confirm credential mappings and activate the workflows.
