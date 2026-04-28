class HTNPlanner:
    def __init__(self, methods, operators):
        self.methods = methods
        self.operators = operators
        self.tree = []

    def plan(self, tasks, state):
        plan = []
        success = self._seek_plan(tasks, state, plan, "ROOT")
        if success:
            return plan
        return None

    def _seek_plan(self, tasks, state, plan, parent):
        if not tasks:
            return True

        task = tasks[0]
        remaining = tasks[1:]

        task_name = task[0]

        if task_name in self.operators:
            precond, effect = self.operators[task_name]

            if precond(state, *task[1:]):
                self.tree.append((parent, task_name))
                effect(state, *task[1:])
                plan.append(task)
                return self._seek_plan(remaining, state, plan, task_name)
            else:
                return False

        if task_name in self.methods:
            for method in self.methods[task_name]:
                name, precond, subtasks = method

                if precond(state, *task[1:]):
                    self.tree.append((parent, task_name))
                    self.tree.append((task_name, name))

                    new_tasks = subtasks(state, *task[1:]) + remaining

                    if self._seek_plan(new_tasks, state, plan, name):
                        return True

        return False