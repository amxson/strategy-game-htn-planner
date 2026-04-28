from htn_engine import HTNPlanner
from domain import methods, operators, initial_state
from tree_visualizer import print_decomposition_tree


def print_plan(plan):
    print("\nFINAL PRIMITIVE PLAN")
    print("--------------------")

    if not plan:
        print("No valid plan found.")
        return

    for i, task in enumerate(plan, start=1):
        print(f"Step {i}: {task[0]}")


def print_state(state):
    print("\nFINAL WORLD STATE")
    print("-----------------")

    for key, value in state.items():
        print(f"{key}: {value}")


def main():
    state = initial_state.copy()

    planner = HTNPlanner(methods, operators)

    goal = [("ProtectVillage",)]

    plan = planner.plan(goal, state)

    print_plan(plan)
    print_decomposition_tree(planner.tree)
    print_state(state)


if __name__ == "__main__":
    main()