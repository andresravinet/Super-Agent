# Prompts

Prompt templates and conversation scaffolding for agent nodes live here.

## Purpose
- Store reusable system/user prompts for n8n `openAIAssistant` nodes so they can be iterated without editing workflow JSON by hand.
- Keep variants of the same prompt visible to reviewers before embedding them into `workflows/*.json`.

## Required file types
- Markdown (`.md`) or plain text (`.txt`) for authored prompts.
- JSON snippets (`.json`) when a prompt needs structured metadata (for example, role definitions or tool-call hints) before being copied into a node.

## Naming and versioning
- Name files by role and scope using kebab-case, e.g., `router-system-v1.md` or `specialist-comms-followup.txt`.
- Increment the suffix (`-v2`, `-2024-09`) when changing intent classification rules or tool-call guidance; keep the previous version to preserve history for audits.
- Inside each file, include a short header noting which workflow node uses it (for example, `Used by workflows/router.json -> AI Router`).

## Producing and consuming artifacts
- Author prompts in this directory first, then paste the final text into the relevant `openAIAssistant` node inside the workflow export.
- When exporting updated workflows from n8n, ensure the embedded prompt matches the latest file revision noted above.
- If prompts include JSON examples, validate them against the schemas in `schemas/` (e.g., `schemas/request_envelope.json`) so they align with test fixtures.

## Examples
- Router system prompt: draft `router-system-v1.md` that describes allowed intents and specialists, then embed it into the `AI Router` node in `workflows/router.json`.
- Planner prompt: author `planner-system-v1.md` with approval-handling guidance before updating the `Planner Agent` node in `workflows/main_orchestrator.json`.
