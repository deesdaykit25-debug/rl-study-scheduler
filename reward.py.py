def compute_reward(state, action, task=None):
    reward = 0

    if action == "DO_TASK" and task:
        reward += 10
        if task["difficulty"] > 7:
            reward += 5
        # bonus for completing urgent tasks
        if task["deadline"] < 2:
            reward += 4

    for t in state["tasks"]:
        if not t["completed"] and t["deadline"] <= 0:
            reward -= 8

    if state["student"]["stress"] > 80:
        reward -= 5

    if state["student"]["energy"] < 20:
        reward -= 10

    if action == "SWITCH":
        reward -= 2

    if action == "SKIP":
        reward -= 3

    if action == "BREAK":
        reward += 2

    return reward
