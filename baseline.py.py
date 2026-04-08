def heuristic_policy(state):
    tasks = [t for t in state["tasks"] if not t["completed"]]

    if not tasks:
        return "BREAK"

    tasks.sort(key=lambda t: (t["deadline"], -t["importance"]))

    if state["student"]["energy"] < 30:
        return "BREAK"

    return "DO_TASK"
