import json
import unittest
from pathlib import Path

import jsonschema
from jsonschema import RefResolver


class WorkflowHarnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parent.parent
        cls.workflows_dir = cls.root / "workflows"
        cls.schemas_dir = cls.root / "schemas"
        cls.fixtures_dir = cls.root / "tests" / "fixtures"

    def load_json(self, path: Path):
        with path.open() as handle:
            return json.load(handle)

    def schema_path(self, name: str) -> Path:
        return self.schemas_dir / f"{name}.json"

    def schema(self, name: str):
        return self.load_json(self.schema_path(name))

    def fixture(self, name: str):
        return self.load_json(self.fixtures_dir / name)

    def workflow(self, name: str):
        return self.load_json(self.workflows_dir / name)

    def validate_schema(self, instance: dict, schema_path: Path):
        schema = self.load_json(schema_path)
        base_uri = schema_path.resolve().as_uri()
        resolver = RefResolver(base_uri=base_uri, referrer=schema)
        jsonschema.Draft202012Validator(schema, resolver=resolver).validate(instance)

    def test_request_and_plan_conform_to_schema(self):
        request_envelope = self.fixture("request_envelope.json")
        router_plan = self.fixture("router_plan.json")

        self.validate_schema(request_envelope, self.schema_path("request_envelope"))
        self.validate_schema(router_plan, self.schema_path("router_plan"))

    def test_specialist_outputs_conform_to_schema(self):
        specialist_result = self.fixture("specialist_result.json")
        tool_schema = self.schema("tool_call")

        self.validate_schema(specialist_result, self.schema_path("specialist_result"))
        for tool_call in specialist_result["tool_calls"]:
            self.validate_schema(tool_call, self.schema_path("tool_call"))
            jsonschema.validate(instance=tool_call, schema=tool_schema)

    def test_tool_call_fixtures_respect_schema(self):
        read_call = self.fixture("tool_call_read.json")
        write_call = self.fixture("tool_call_write.json")

        self.validate_schema(read_call, self.schema_path("tool_call"))
        self.validate_schema(write_call, self.schema_path("tool_call"))

    def test_router_routing_table_matches_known_intents(self):
        router_workflow = self.workflow("router.json")
        request_schema = self.schema("request_envelope")
        router_schema = self.schema("router_plan")

        intents = set(request_schema["properties"]["intent"]["enum"])
        specialists = set(router_schema["properties"]["specialist"]["enum"])

        self.assertEqual(set(router_workflow["routing_table"].keys()), intents)
        self.assertTrue(set(router_workflow["routing_table"].values()).issubset(specialists))

    def test_approval_gate_for_write_side_effects(self):
        orchestrator = self.workflow("main_orchestrator.json")
        approval_workflow_name = orchestrator["policies"]["approval_workflow"]
        approval_step = next(
            (step for step in orchestrator["flow"] if step.get("id") == approval_workflow_name),
            None,
        )
        required_effects = set(orchestrator["policies"]["requires_approval_for"])

        read_call = self.fixture("tool_call_read.json")
        write_call = self.fixture("tool_call_write.json")

        def needs_approval(tool_call: dict) -> bool:
            return bool(set(tool_call["expected_side_effects"]) & required_effects)

        self.assertIsNotNone(approval_step, "Approval gate step should be defined in the orchestrator flow")
        self.assertEqual(approval_step["uses"], approval_workflow_name)
        self.assertFalse(needs_approval(read_call), "Read-only tool calls should bypass approval")
        self.assertTrue(needs_approval(write_call), "Write or external calls should require approval")

    def test_replay_gathers_expected_outputs(self):
        orchestrator = self.workflow("main_orchestrator.json")
        router_plan = self.fixture("router_plan.json")
        approval_gate = self.workflow("approval_gate.json")

        approval_required = bool(
            set(router_plan["side_effects"]) & set(orchestrator["policies"]["requires_approval_for"])
        )
        self.assertTrue(approval_required, "Router plan fixture should require approval to exercise the gate")
        self.assertIn("criteria", approval_gate)
        self.assertIn("requires_manual_review", approval_gate["criteria"])


if __name__ == "__main__":
    unittest.main()
