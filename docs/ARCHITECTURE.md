# System Architecture

This document outlines the intended orchestration flow for the Super-Agent platform.

## Flow Overview

Intake → Router → Specialist → Tools → Approval → Execute → Log

## Intake options

- **Chat trigger**: User messages arrive via n8n Webhook or Chat trigger nodes and are normalized into the `schemas/request_envelope.json` shape. Authentication and anti-abuse checks (rate limiting, IP allowlists) run before the payload reaches the router.
- **Webhook trigger**: External systems post JSON envelopes that include tenant metadata and requested capability. The webhook node applies HMAC verification and maps headers/body fields into the same normalized envelope used by chat traffic.
- **Shared behaviors**: Both paths attach a request ID, user/tenant identifiers, and any upstream moderation flags so downstream nodes can enforce policy without re-validating raw inputs.

## Router and specialist configuration

- **Router** (`workflows/router.json`)
  - Consumes the normalized envelope and classifies it into an intent plus target specialist.
  - Applies policy filters (blocked intents, maintenance windows) and enriches the plan with tool needs and approval hints.
  - Emits a `router_plan` object conforming to `schemas/router_plan.json`, which the orchestrator passes unchanged to the specialist lane.
- **Specialists** (`workflows/specialist_*.json`)
  - Each specialist (ops, scheduling, research, comms) receives the router plan and executes domain-specific prompting/planning.
  - Specialists select tools and produce a structured `specialist_output` matching `schemas/specialist_output.json`, including planned tool calls and human-readable rationales.
  - Optional safety hooks can downgrade or re-route plans (e.g., escalate to approval) before any tool execution.

## Schema-to-node output mapping

- **Router output → Specialist input**: The router node must emit `intent`, `target_specialist`, and `context` fields exactly as defined in `schemas/router_plan.json`. The orchestrator injects this object into the specialist workflow without modification.
- **Specialist output → Tool runner**: Specialists produce `planned_tools[]` entries with `name`, `parameters`, `read_only`, and `requires_approval` flags per `schemas/specialist_output.json`. The tool runner node iterates over this list and maps each entry into sub-workflow calls.
- **Tool results → Approval gate**: Tool sub-workflows return `status`, `result`, and `side_effects` fields that conform to `schemas/tool_result.json`. The approval gate evaluates these outputs alongside the planned intent to decide whether to proceed, pause for human review, or abort.

## Tool sub-workflow calls

- Sub-workflows live under `workflows/tools/` and are invoked by the orchestrator or specialist lanes via n8n **Execute Workflow** nodes.
- Calls are parameterized with the `parameters` object from `planned_tools[]`, and the parent workflow awaits structured responses before continuing.
- Retryable tools (idempotent reads) enable n8n’s built-in retry/backoff; non-idempotent writes rely on the approval gate before execution.

## Approval gate mechanics

- The approval gate (`workflows/approval_gate.json`) receives the planned action, tool payloads, and any moderation flags.
- It evaluates risk (PII presence, write/external side effects, tenant policy) and either:
  - Auto-approves low-risk read operations.
  - Pauses for human review via task/notification nodes when thresholds are exceeded.
  - Rejects execution outright when policies are violated (blocked domains, missing consent, or safety classifier failures).
- Approved actions rejoin the orchestrator path and proceed to execution; rejected actions return structured errors to the requester.

## Logging and audit

- Every workflow attaches the request ID and tenant/user identifiers to log entries and tool invocations.
- Node outputs (router decisions, specialist plans, tool responses, approval outcomes) are persisted to a centralized log sink (e.g., database table or log stream) with timestamps and versioned workflow IDs.
- Audit trails include the exact prompt/tool payloads and approval decisions to support replay via `tests/test_workflows.py` fixtures.

## Environment separation

- **dev**: Fast iteration with synthetic credentials and verbose logging. Uses `N8N_IMPORT_OPTS` with `--separate --force` for rapid imports.
- **stage**: Mirrors production credentials but scoped to test tenants. Approval gate defaults to “review required” for all write/external actions.
- **prod**: Hardened configuration with strict webhook verification, minimal logging of sensitive fields, and approval rules tuned per tenant. Imports run from pinned tags and require passing schema/tests before promotion.
- Configuration differences are captured via environment variables and n8n credential sets; workflow JSON remains shared but parameterized per environment.

## Data passing sequence

1. **Intake**: Chat/Webhook trigger normalizes the envelope and assigns `request_id`.
2. **Router**: Classifies intent → emits `router_plan`.
3. **Specialist**: Consumes `router_plan` → produces `specialist_output` with `planned_tools`.
4. **Tool runner**: Invokes sub-workflows for each planned tool → collects `tool_result` objects.
5. **Approval gate**: Evaluates `router_plan`, `specialist_output`, and `tool_result` side effects → approve, request review, or reject.
6. **Execute**: Executes approved actions (or surfaces approval tasks) and aggregates final response.
7. **Log**: Persists all structured artifacts (plans, tool payloads, approvals) tagged with `request_id` for audit and replay.

## Error handling and retries

- **Router/Specialist errors**: Validation failures on schema mismatch return a structured error payload upstream; intake surfaces a user-friendly message while logging full details.
- **Tool errors**: Idempotent tools use n8n retry with exponential backoff. Non-idempotent tools surface errors without retry and mark the plan as requiring operator intervention.
- **Approval timeouts**: Human-review waits have timeouts that auto-expire to a safe default (reject or re-queue) and notify operators.
- **Circuit breakers**: Repeated failures on the same tool/tenant can trigger temporary routing blocks or fall back to read-only responses.

## Components and Responsibilities

- **Intake**
  - Receive raw user requests from API, CLI, or UI surfaces.
  - Normalize inputs (authentication, formatting, and safety checks) before routing.
- **Router**
  - Classify intents and select the appropriate specialist pipeline.
  - Apply routing policies, priorities, and guardrails.
- **Specialist**
  - Provide domain-specific reasoning and planning for the routed task.
  - Decompose work into actionable steps and select needed tools.
- **Tools**
  - Execute external actions such as API calls, database queries, or code generation.
  - Return structured results and errors to the invoking specialist.
- **Approval**
  - Validate planned or proposed actions against policy and risk thresholds.
  - Gather human or automated approval signals before execution when required.
- **Execute**
  - Carry out approved actions and orchestrate side effects.
  - Handle retries and rollback/compensation logic as needed.
- **Log**
  - Persist conversation history, decisions, tool invocations, and outcomes.
  - Emit analytics and audit trails for observability and compliance.
