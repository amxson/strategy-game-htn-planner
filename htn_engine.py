from copy import deepcopy


class HTNPlanner:
    def __init__(self, methods, operators, max_depth=200):
        self.methods = methods
        self.operators = operators
        self.max_depth = max_depth
        self.tree = []

    def plan(self, tasks, state):
        """Commit a successful branch; leave caller state unchanged on failure."""
        self.tree = []
        result = self._seek_plan(tasks, deepcopy(state), [], [], "ROOT", 0)
        if result is None:
            return None
        plan, final_state, tree = result
        state.clear()
        state.update(final_state)
        self.tree = tree
        return plan

    def _seek_plan(self, tasks, state, plan, tree, parent, depth):
        if not tasks:
            return plan, state, tree
        if depth >= self.max_depth:
            return None
        task, remaining = tasks[0], tasks[1:]
        name = task[0]
        if name in self.operators:
            precondition, effect = self.operators[name]
            branch = deepcopy(state)
            if precondition(branch, *task[1:]):
                effect(branch, *task[1:])
                return self._seek_plan(
                    remaining,
                    branch,
                    plan + [task],
                    tree + [(parent, name)],
                    name,
                    depth + 1,
                )
            return None
        for method_name, precondition, subtasks in self.methods.get(name, []):
            branch = deepcopy(state)
            if precondition(branch, *task[1:]):
                result = self._seek_plan(
                    subtasks(branch, *task[1:]) + remaining,
                    branch,
                    plan[:],
                    tree + [(parent, name), (name, method_name)],
                    method_name,
                    depth + 1,
                )
                if result is not None:
                    return result
        return None
