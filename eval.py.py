def evaluate(state):
    tasks = state["tasks"]

    completed = sum(1 for t in tasks if t["completed"])
    missed = sum(1 for t in tasks if not t["completed"] and t["deadline"] <= 0)

    avg_stress = state["student"]["stress"]
    efficiency = completed / len(tasks) if len(tasks) > 0 else 0

    return {
        "tasks_completed": completed,
        "missed_deadlines": missed,
        "avg_stress": avg_stress,
        "efficiency_score": round(efficiency, 2),
        "total_tasks": len(tasks)
    }
