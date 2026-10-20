import unittest
from htn_engine import HTNPlanner
from domain import methods, operators, initial_state


class PlannerTests(unittest.TestCase):
    def test_demo_reaches_goal(self):
        state = initial_state.copy()
        self.assertIsNotNone(
            HTNPlanner(methods, operators).plan([("ProtectVillage",)], state)
        )
        self.assertTrue(state["mission_complete"])

    def test_failed_branch_does_not_leak_state_plan_or_tree(self):
        ops = {
            "spend": (lambda s: True, lambda s: s["items"].append("spent")),
            "fail": (lambda s: False, lambda s: None),
            "finish": (lambda s: not s["items"], lambda s: s.update(done=True)),
        }
        methods = {
            "goal": [
                ("bad", lambda s: True, lambda s: [("spend",), ("fail",)]),
                ("good", lambda s: True, lambda s: [("finish",)]),
            ]
        }
        state = {"items": []}
        planner = HTNPlanner(methods, ops)
        self.assertEqual(planner.plan([("goal",)], state), [("finish",)])
        self.assertEqual(state, {"items": [], "done": True})
        self.assertNotIn(("goal", "bad"), planner.tree)
        self.assertEqual(planner.plan([], state), [])
        self.assertEqual(planner.tree, [])

    def test_failure_does_not_mutate_caller(self):
        state = {"items": []}
        planner = HTNPlanner(
            {}, {"spend": (lambda s: True, lambda s: s["items"].append(1))}
        )
        self.assertIsNone(planner.plan([("spend",), ("unknown",)], state))
        self.assertEqual(state, {"items": []})
        self.assertEqual(planner.tree, [])

    def test_recursive_method_has_a_depth_bound(self):
        planner = HTNPlanner(
            {"loop": [("again", lambda s: True, lambda s: [("loop",)])]},
            {},
            max_depth=5,
        )
        self.assertIsNone(planner.plan([("loop",)], {}))


if __name__ == "__main__":
    unittest.main()
